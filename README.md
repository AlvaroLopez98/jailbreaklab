# JailbreakLab

Sistema de deteccion y mitigacion de ataques de jailbreak y prompt injection en IA conversacional.

## Descripcion

JailbreakLab es un prototipo de seguridad desarrollado como TFG del ciclo DAM. Actua como capa intermedia entre el usuario y el modelo de IA, analizando cada mensaje antes de enviarlo y bloqueando intentos de manipulacion.

## Caracteristicas

- Analisis de prompts mediante reglas y expresiones regulares
- Puntuacion de riesgo: bajo, medio y alto
- Integracion con Groq API (llama-3.3-70b-versatile)
- Registro de analisis en SQLite
- API REST documentada con FastAPI

## Instalacion

    git clone https://github.com/AlvaroLopez98/jailbreaklab
    cd jailbreaklab
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Crea un archivo .env con tu clave de Groq: GROQ_API_KEY=tu_clave_aqui

## Uso

    uvicorn main:app --reload

Documentacion interactiva: http://127.0.0.1:8000/docs

## Endpoints

- GET / — Estado de la API
- POST /analyze — Analiza un prompt
- GET /registros — Historial de analisis

## Tecnologias

- Python 3.12 + FastAPI
- Groq API
- SQLite
- WSL2 Ubuntu
