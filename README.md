# Operación Eco del Búnker

Este proyecto corresponde a una API desarrollada para resolver el desafío de programación "Operación Eco del Búnker".

La aplicación permite calcular la posición de un convoy usando las distancias recibidas por tres antenas y reconstruir el mensaje fragmentado recibido por cada una.

## Tecnologías utilizadas

Utilicé Python con FastAPI porque permite crear APIs REST de forma r+apida y simple. Además, FastAPI genera documentación automática en '/docs', lo que facilita probar los endpoints sin usar herramientas externas.

También se usó Uvicorn para levantar el servidor localmente.

## Cómo ejecutar el proyecto localmente

Primero se debe clonar o descargar el proyecto y entrar en la carpeta.

```bash
git clone https://github.com/Pygc/Desafio_pSIGA.git
cd Desafio_pSIGA
```

Crear entorno virtual: 

```bash
    python -m venv venv
```

Activar el entorno virtual en Git Bash:

```bash
pip install -r requirements.txt
```

Ejecutar el proyecto:

```bash
uvicorn main:app --reload
```

Luego abrir en el navegador:

```txt
http://127.0.0.1:8000/docs
```

La interfaz web simple está disponible en:

```txt
http://127.0.0.1:8000/ui
```

## Endpoints principales

### GET /

Permite verificar que la API está funcionando.

### POST /survival/

Recibe la información completa de las tres antenas y retorna la posición calculada junto con el mensaje reconstruido.

### POST /survival_split/{antenna_name}

Permite guardar la información de una antena específica. Los nombres válidos son `alpha`, `beta` y `omega`.

### GET /survival_split/

Intenta calcular la posición y reconstruir el mensaje usando los datos guardados previamente.

## Consideraciones

Los datos de `/survival_split/` se guardan en memoria, por lo que se pierden al reiniciar el servidor.

Para este desafío lo dejé así por simplicidad, pero en una versión productiva, esta información debería guardarse en una base de datos.

También se manejan errores con código 404 cuando no hay información suficiente para calcular la posición o reconstruir el mensaje.

## Docker

No incluí Docker en esta versión, ya que no lo he utilizado antes (aprenderé ahora), pero la ejecución local con entorno virtual es suficiente para levantar y probar el proyecto.

## Pruebas 

La solución fue probaba manualmente usando la documentación automática de FastAPI en `/docs`, validando casos exitosos y casos de error como antenas faltantes, mensajes incompletos y antenas desconocidas.

## Nota sobre las coordenadas y distancias del ejemplo

Durante las pruebas observé que las distancias indicadas en el ejemplo del enunciado no son matemáticamente consistentes con la posición esperada.

El enunciado usa estas distancias:

```txt
alpha: 100.0
beta: 115.5
omega: 142.7
```
pero para la posición esperada aproximada:

x: -100.0
y: 75.5

las distancias reales aproximadas desde las antenas son:

alpha: 485.91
beta: 266.02
omega: 600.50

Por esta razón, para validar el cálculo de posición utilicé distancias coherentes con las coordenadas esperadas. El algoritmo de trilateración funciona con las coordenadas fijas de las antenas y las distancias entregadas en la solicitud.

# Cómo utilizar/probar el nivel 1

Desde la documentación automática de FastAPI: http://127.0.0.1:8000/docs

Buscar el endpoint: POST /survival/

Presionar `Try it out` y usa el siguiente JSON:

{
  "antennas": [
    {
      "name": "alpha",
      "distance": 485.91,
      "message": ["necesitamos", "", "", "suministros", ""]
    },
    {
      "name": "beta",
      "distance": 266.02,
      "message": ["", "ayuda", "", "", "medicos"]
    },
    {
      "name": "omega",
      "distance": 600.50,
      "message": ["necesitamos", "", "con", "", ""]
    }
  ]
}

Presionar: `Execute`

Respuesta esperada:

{
  "position": {
    "x": -99.68,
    "y": 74.77
  },
  "message": "necesitamos ayuda con suministros medicos"
}

# Cómo utilizar/probar el nivel 2

El Nivel 2 permite registrar la información de cada antena por separado.

Primero ingresar a: http://127.0.0.1:8000/docs

1) Registrar `alpha`

Buscar el endpoint: POST /survival_split/{antenna_name}

En `antenna_name` escribir: `alpha`

Luego en Body: 

{
  "distance": 485.91,
  "message": ["necesitamos", "", "", "suministros", ""]
}

Presionar: `Execute`.

2) Registrar `beta`

En `antenna_name` escribir: `beta`

Luego en Body: 

{
  "distance": 266.02,
  "message": ["", "ayuda", "", "", "medicos"]
}

Presionar: `Execute`.

3) Registrar `omega`

En `antenna_name` escribir: `omega`

Luego en Body: 

{
  "distance": 600.50,
  "message": ["necesitamos", "", "con", "", ""]
}

Presionar: `Execute`.

4) Obtener resultado final

Buscar el endpoint: GET /survival_split/

Presionar `Try it out` y luego `Execute`.

Respuesta esperada:

{
  "position": {
    "x": -99.68,
    "y": 74.77
  },
  "message": "necesitamos ayuda con suministros medicos"
}

(Si falta registrar alguna antena, el endpoint responderá con error indicando qué datos faltan)

### Pruebas

a) Prueba 1: `Get /survival_split/` sin datos.

(Primero se limpia los datos reiniciando Uvicorn)

Luego en /docs, sin haber hecho ningún POST, ejecuta: 
        `Get /survival_split/`

Dará una respuesta de error 404:

{
  "detail": {
    "message": "Faltan datos para calcular la posición y el mensaje",
    "missing_antennas": ["alpha", "beta", "omega"]
  }
}

Eso prueba que la API detecta cuando faltan antenas.

b) Prueba 2: `POST /survival_split/{antenna_name}` con antena inválida.

En el campo `antenna_name`, se escribo: gamma

En el Body pongo (JSON):

{
  "distance": 100,
  "message": ["hola"]
}

Y lo ejecuto.

Dará una respuesta de error 404:

{
  "detail": "Antena desconocida"
}

Eso prueba que la API rechaza antenas que no sean `alpha`, `beta` u `omega`.

c) Prueba 3: `POST /survival/` con mensaje incompleto.

En el body pongo:

{
  "antennas": [
    {
      "name": "alpha",
      "distance": 485.91,
      "message": ["necesitamos", "", "", "", ""]
    },
    {
      "name": "beta",
      "distance": 266.02,
      "message": ["", "ayuda", "", "", ""]
    },
    {
      "name": "omega",
      "distance": 600.50,
      "message": ["", "", "con", "", ""]
    }
  ]
}

Y lo ejecuto.

Dará una respuesta de error 404:

{
  "detail": "No se pudo reconstruir el mensaje completo"
}

Eso prueba que la API detecta cuando no puede armar el mensaje completo.

d) Prueba 4: `POST /survival/` con antena faltante.

Pongo este body, (que solo tiene dos antenas):

{
  "antennas": [
    {
      "name": "alpha",
      "distance": 485.91,
      "message": ["necesitamos", "", "", "suministros", ""]
    },
    {
      "name": "beta",
      "distance": 266.02,
      "message": ["", "ayuda", "", "", "medicos"]
    }
  ]
}

Y lo ejecuto.

Dará una respuesta de error 404:

{
  "detail": "Se necesitan las 3 antenas"
}

e) Prueba 5: flujo correcto después de errores.

En `POST /survival/`, pongo este body:

{
  "antennas": [
    {
      "name": "alpha",
      "distance": 485.91,
      "message": ["necesitamos", "", "", "suministros", ""]
    },
    {
      "name": "beta",
      "distance": 266.02,
      "message": ["", "ayuda", "", "", "medicos"]
    },
    {
      "name": "omega",
      "distance": 600.50,
      "message": ["necesitamos", "", "con", "", ""]
    }
  ]
}

Dará una respuesta 200:

{
  "position": {
    "x": -99.68,
    "y": 74.77
  },
  "message": "necesitamos ayuda con suministros medicos"
}

## Cómo utilizar la interfaz (Probar nivel 3)

1) Primero registra `alpha`.

Antena: alpha
Distancia: 485.91
Mensaje (JSON): ["necesitamos", "", "", "suministros", ""]

Presiona: Guardar antena

2) Luego registra `beta`.

Antena: beta
Distancia: 266.02
Mensaje (JSON): ["", "ayuda", "", "", "medicos"]

Presiona: Guardar antena

3) Luego registra `omega`.

Antena: omega
Distancia: 600.50
Mensaje (JSON): ["necesitamos", "", "con", "", ""]

Presiona: Guardar antena

4) Finalmente presiona: Calcular posición y mensaje

Y te mostrará en la "Respuesta" (JSON):

{
  "position": {
    "x": -99.68,
    "y": 74.77
  },
  "message": "necesitamos ayuda con suministros medicos"
}