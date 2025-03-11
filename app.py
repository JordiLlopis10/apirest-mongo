from bson import ObjectId
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

app = Flask(__name__)

def get_db():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi("1"))
    return client["test1"]

@app.route("/")
def show():
    db = get_db()
    data = list(db.users.find())
    
    for i in data:
        i["_id"] = str(i["_id"])
    
    return jsonify({"mensaje": data})

@app.route("/add", methods=["POST"])
def add():
    db = get_db()
    datos = request.get_json()
    nombre = datos.get("nombre")
    edad = datos.get("edad")
    
    if nombre and edad:
        resultado = db.users.insert_one({"nombre": nombre, "edad": edad}).inserted_id
        if resultado:
            return jsonify({"Añadido correctamente": str(resultado)})
        else:
            return jsonify({"Mensaje": "No añadido, pringao"})
    
    return jsonify({"mensaje": nombre, "edad": edad})

@app.route("/user/<string:id>", methods=["PUT"])
def actualizar(id):
    db = get_db()
    datos = request.get_json()
    nombre = datos.get("nombre")
    edad = datos.get("edad")

    if nombre and edad:
        resultado = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"nombre": nombre, "edad": edad}}
        )
        if resultado.modified_count > 0:
            return jsonify({"Mensaje": "Actualizado correctamente"})
        else:
            return jsonify({"Mensaje": "No actualizado, pringao"})
            
@app.route("/delete/<string:id>", methods=["DELETE"])
def delete(id):
    db = get_db()
    try:
        resultado = db.users.delete_one({"_id": ObjectId(id)})
        if resultado.deleted_count > 0:
            return jsonify({"Mensaje": "Eliminado correctamente"})
        else:
            return jsonify({"Mensaje": "No se encontró el usuario"})
    except Exception as e:
        return jsonify({"Error": str(e)})

#if __name__ == "__main__":
 #   port = int(os.environ.get("PORT", 10000))  # Render usa un puerto dinámico
  #  app.run(host='0.0.0.0', port=port)
