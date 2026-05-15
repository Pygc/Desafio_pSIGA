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

## Falta por Desarrollar/Solucionar

En cuanto a la interfaz, falta solucionar resultados en botón "Guardar" y "Calcular posición y mensaje".