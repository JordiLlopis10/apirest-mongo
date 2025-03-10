from bson import ObjectId
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

app = Flask(__name__)

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["test1"]



@app.route("/")
def show():
    
    data = list(db.users.find())
    
    for i in data:
        i["_id"] = str(i["_id"])
    
    return jsonify({"mensaje":data})

@app.route("/add", methods=["POST"])
def add():
    datos = request.get_json()
    nombre = datos["nombre"]
    edad = datos["edad"]
    
    if nombre and edad:
        resultado = db.users.insert_one({"nombre":nombre,"edad":edad}).inserted_id
        if resultado:
            return jsonify({"Añadido correctamente":str(resultado)})
        else:
            return jsonify({"Mensaje":"No añadido, pringao"})
    
    return jsonify({"mensaje":nombre,"edad":edad})
    
@app.route("/user/<string:id>", methods=["PUT"])
def actualizar(id):
    datos = request.get_json()
    nombre = datos["nombre"]
    edad = datos["edad"]
    if nombre and edad:
        resultado = db.users.update_one({"_id":ObjectId(id)},{"$set":{"nombre":nombre,"edad":edad}})
        if resultado:
            return jsonify({"Mensaje":"Actualizado correctamente"})
        else:
            return jsonify({"Mensaje":"No actualizado, pringao"})
            
            
@app.route("/delete/<string:id>", methods=["DELETE"])
def delete(id):
    
    try:
        dato = db.users.delete_one({"_id":ObjectId(id)})
        return jsonify({"Mensaje":"Eliminado correctamente"})
    
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run()