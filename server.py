from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Dict, Optional

app = FastAPI()

# Configuración de CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],   # Permitir todos los encabezados
)

class HelloRequest(BaseModel):
    name: str

class HelloReply(BaseModel):
    message: Optional[Dict]  # Cambia el tipo a Dict para manejar datos JSON

def findByCode(code: str):
    uri = "mongodb+srv://calderonhaldor385:Vp9Szac8E3nvDEWZ@so.de31nf8.mongodb.net/"
    client = MongoClient(uri)
    db = client['test']
    collection = db['usuarios']
    resultado = collection.find_one({"codeUTP": code})
    client.close()
    return resultado

def log_message(message: Dict):
    print(f"Mensaje registrado en segundo plano: {message}")

@app.post("/sayhello/", response_model=HelloReply)
async def say_hello(request: HelloRequest, background_tasks: BackgroundTasks):
    try:
        print("Solicitud Recibida")
        resultado = findByCode(request.name)
        
        if resultado:
            resultado['_id'] = str(resultado['_id'])  # Convertimos ObjectId a string
            message = resultado
        else:
            message = {"error": "No se encontró el código"}
        
        background_tasks.add_task(log_message, message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return {"message": message}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
