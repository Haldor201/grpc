from pymongo import MongoClient

def findByCode(code: str):
    uri = "mongodb+srv://calderonhaldor385:Vp9Szac8E3nvDEWZ@so.de31nf8.mongodb.net/"
    client = MongoClient(uri)
    db = client['test']
    collection = db['usuarios']
    resultado = collection.find_one({"codeUTP": code})
    client.close()
    return resultado
