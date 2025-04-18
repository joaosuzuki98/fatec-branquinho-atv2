from datetime import datetime
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()
uri = os.getenv('MONGODB_URL_LOCAL')

# Create a new client and connect to the server
client = MongoClient(uri)
global db
db = client.mercadolivre

def create_compra():
    global db
    mycol = db.compra
    print("\nInserindo uma nova compra")

    produto_id = input("ID do produto: ")
    usuario_id = input("ID do usuário: ")

    produto = db.produto.find_one({ "_id": ObjectId(produto_id) })
    if not produto:
        print("Produto não encontrado.")
        return

    usuario = db.usuario.find_one({ "_id": ObjectId(usuario_id) })
    if not usuario:
        print("Usuário não encontrado.")
        return

    compra_doc = {
        "data": datetime.now(),
        "produto": {
            "id": produto["_id"],
            "nome": produto["nome"],
            "preco_unitario": produto["preco_unitario"]
        },
        "usuario": {
            "id": usuario["_id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "endereco": usuario.get("endereco", ""),
            "cpf": usuario.get("cpf", "")
        },
        "vendedor": {
            "id": produto["vendedor"]["_id"],
            "nome": produto["vendedor"]["nome"],
            "cnpj": produto["vendedor"].get("cnpj", ""),
            "cpf": produto["vendedor"].get("cpf", ""),
            "cep": produto["vendedor"].get("cep", "")
        }
    }

    x = mycol.insert_one(compra_doc)
    print("Compra registrada com ID", x.inserted_id)


def read_compra(nome_usuario=""):
    global db
    mycol = db.compra
    print("\nCompras registradas:")

    if nome_usuario:
        myquery = { "usuario.nome": nome_usuario }
        compras = mycol.find(myquery)
    else:
        compras = mycol.find()

    for compra in compras:
        print(f"ID: {compra['_id']}, Produto: {compra['produto']['nome']} - R${compra['produto']['preco_unitario']}, "
              f"Usuário: {compra['usuario']['nome']}, Data: {compra['data'].strftime('%d/%m/%Y %H:%M:%S')}")


def update_compra(compra_id):
    global db
    mycol = db.compra
    compra = mycol.find_one({ "_id": ObjectId(compra_id) })

    if not compra:
        print("Compra não encontrada.")
        return

    print("Compra atual:", compra)

    produto_id = input("Novo ID do produto (deixe em branco para manter): ")
    if produto_id:
        produto = db.produto.find_one({ "_id": ObjectId(produto_id) })
        if not produto:
            print("Produto não encontrado.")
            return
        compra["produto"] = {
            "id": produto["_id"],
            "nome": produto["nome"],
            "preco_unitario": produto["preco_unitario"]
        }
        compra["vendedor"] = {
            "id": produto["vendedor"]["_id"],
            "nome": produto["vendedor"]["nome"],
            "cnpj": produto["vendedor"].get("cnpj", ""),
            "cpf": produto["vendedor"].get("cpf", ""),
            "cep": produto["vendedor"].get("cep", "")
        }

    usuario_id = input("Novo ID do usuário (deixe em branco para manter): ")
    if usuario_id:
        usuario = db.usuario.find_one({ "_id": ObjectId(usuario_id) })
        if not usuario:
            print("Usuário não encontrado.")
            return
        compra["usuario"] = {
            "id": usuario["_id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "endereco": usuario.get("endereco", ""),
            "cpf": usuario.get("cpf", "")
        }

    newvalues = { "$set": compra }
    mycol.update_one({ "_id": ObjectId(compra_id) }, newvalues)
    print("Compra atualizada.")


def delete_compra(compra_id):
    global db
    mycol = db.compra
    mycol.delete_one({ "_id": ObjectId(compra_id) })
    print("Compra deletada.")
