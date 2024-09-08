from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Dict, Optional

app = FastAPI()

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

@app.post("/sayhello/", response_model=HelloReply)
async def say_hello(request: HelloRequest):
    try:
        print("Solicitud Recibida")
        resultado = findByCode(request.name)
        
        if resultado:
            resultado['_id'] = str(resultado['_id'])  # Convertimos ObjectId a string
            message = resultado  # Devuelve el diccionario directamente
        else:
            message = {"error": "No se encontró el código"}  # Devuelve un diccionario con un mensaje de error
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return {"message": message}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
