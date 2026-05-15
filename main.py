from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import math

app = FastAPI()

ANTENAS_POSITIONS = {
    "alpha": (-500.0, -200.0),
    "beta": (100.0, -100.0),
    "omega": (500.0, 100.0)
}

stored_antennas = {}

class AntennaInput(BaseModel):
    name: str
    distance: float
    message: List[str]
    
class SurvivalRequest(BaseModel):
    antennas: List[AntennaInput]
    
class SplitRequest(BaseModel):
    distance: float
    message: List[str]
    
def decode_message(messages):
    max_length = 0
    
    for message in messages:
        if len(message) > max_length:
            max_length = len(message)
            
    final_words = []
        
    for index in range(max_length):
        selected_word = ""
        
        for message in messages:
            if index < len(message): 
                word = message[index]
            
                if word != "":
                    selected_word = word        
        final_words.append(selected_word)

    for word in final_words:
        if word == "":
            raise ValueError("No se pudo reconstruir el mensaje completo")
        
    return " ".join(final_words)
    
def validate_distance(x, y, antenna_x, antenna_y, expected_distance):
    calculated_distance = math.sqrt((x - antenna_x) ** 2 + (y - antenna_y) ** 2)
    return abs(calculated_distance - expected_distance) < 1.0

def calculate_position(antennas):
    if len(antennas) < 3:
        raise ValueError("Se necesitan al menos 3 antenas")
    
    distances = {}
    
    for antenna in antennas:
        if antenna.name not in ANTENAS_POSITIONS:
            raise ValueError(f"Antena desconocida: {antenna.name}")
        
        distances[antenna.name] = antenna.distance
        
    required_antennas = ["alpha", "beta", "omega"]
    
    for antenna_name in required_antennas:
        if antenna_name not in distances:
            raise ValueError(f"Falta la antena requerida: {antenna_name}")
        
    x1, y1 = ANTENAS_POSITIONS["alpha"]
    x2, y2 = ANTENAS_POSITIONS["beta"]
    x3, y3 = ANTENAS_POSITIONS["omega"]
    
    r1 = distances["alpha"]
    r2 = distances["beta"]
    r3 = distances["omega"]
    
    a = 2 * (x2 - x1)
    b = 2 * (y2 - y1)
    c = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    
    d = 2 * (x3 - x1)
    e = 2 * (y3 - y1)
    f = r1**2 - r3**2 - x1**2 + x3**2 - y1**2 + y3**2
    
    determinant = a * e - b * d
    
    if determinant == 0:
        raise ValueError("No se puede calcular la posición")
    
    x = (c * e - b * f) / determinant
    y = (a * f - c * d) / determinant
    
    if not validate_distance(x, y, x1, y1, r1):
        raise ValueError("La distancia con alpha no coincide")
    
    if not validate_distance(x, y, x2, y2, r2):
        raise ValueError("La distancia con beta no coincide")
    
    if not validate_distance(x, y, x3, y3, r3):
        raise ValueError("La distancia con omega no coincide")

    return {
        "x": round(x, 2),
        "y": round(y, 2)
    }
    
@app.get("/")
def health_check():
    return {"message": "API funcionando correctamente"}

@app.post("/survival/")
def survival(request: SurvivalRequest):
    messages = []
        
    for antenna in request.antennas: 
        messages.append(antenna.message)

    try:
        position = calculate_position(request.antennas)
        final_message = decode_message(messages)
        
        return {
            "position": position,
            "message": final_message
            }
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

@app.post("/survival_split/{antenna_name}")
def survival_split_post(antenna_name: str, request: SplitRequest):
    if antenna_name not in ANTENAS_POSITIONS:
        raise HTTPException(status_code=404, detail="Antena Desconocida")

    stored_antennas[antenna_name] = AntennaInput(
        name=antenna_name,
        distance=request.distance,
        message=request.message
    )
    
    return {
        "message": f"Información de antena {antenna_name} guardada correctamente"
    }
    
@app.get("/survival_split/")
def survival_split_get():
    missing_antennas = []
    
    for antenna_name in ANTENAS_POSITIONS.keys():
        if antenna_name not in stored_antennas:
            missing_antennas.append(antenna_name)
            
    if len(missing_antennas) > 0:
        return {
            "error": "Faltan datos para calcular la posición y el mensaje",
            "missing_antennas": missing_antennas
        }
        
    antennas = list(stored_antennas.values())
    
    messages = []
    
    for antenna in antennas:
        messages.append(antenna.message)
        
    try:
        position = calculate_position(antennas)
        final_message = decode_message(messages)
        
        return {
            "position": position,
            "message": final_message
        }
    
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    
@app.get("/ui", response_class=HTMLResponse)
def user_interface():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Operación Eco del Búnker</title>
        <style>
            body {
                font-family: Atial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
            }
            
            h1 {
                color: #222;
            }
            
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                max-width: 700px;
            }
            
            label {
                display: block;
                margin-top: 12px;
                font-weight: bold;
            }
            
            input, textarea, select {
                width: 100%;
                padding: 8px;
                margin-top: 4px;
                box-sizing: border-box;
            }
            
            button {
                margin-top: 16px;
                padding: 10px 16px;
                cursor: pointer;
            }
            
            pre {
                background: #222;
                color: #0f0;
                padding: 16px;
                border-radius: 8px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Operación Eco del Búnker</h1>
            
            <h2>Registrar Antena</h2>
            
            <label>Antena</label>
            <select id= "antennaName">
                <option value="alpha">alpha</option>
                <option value="beta">beta</option>
                <option value="omega">omega</option>
            </select>
            
            <label>Distancia</label>
            <input id= "distance" type="number" step="0.01" placeholder= "Ej: 485.91">
            
            <label>Mensaje</label>
            <textarea id= "message" rows="3" placeholder= 'Ej: ["necesitamos", "", "", "suministros", ""]'></textarea>
            
            <button onclick="saveAntenna()">Guardar antena</button>
            <button onclick="calculate()">Calcular posición y mensaje</button>
            
            <h2>Respuesta</h2>
            <pre id="result">Esperando datos...</pre>
        </div>
        
        <script>
            async function saveAntenna() {
                const antennaName = document.getElementById("antennaName").value;
                const distance = parseFloat(document.getElementById("distance").value);
                const messageText = document.getElemenById("message").value;
                
                let message;
                
                try {
                    message = JSON.parse(messageText);
                } catch (error) {
                    document.getElementById("result").textContent = "El mensaje debe ser un arreglo JSON válido.";
                    return;
                }
                
                const response = await fetch(`/survival_split/${antennaName}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        distance: distance,
                        message: message
                    })
                });
                
                const data = await response.json();
                document.getElementById("result").textContent = JSON.stringify(data, null, 2);
            }
            
            async function calculate() {
                const response = await fetch("/survival_split/");
                const data = await response.json();
                document.getElementById("result").textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """