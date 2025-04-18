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

def create_favorito():
    global db
    mycol = db.favorito
    print("\nInserindo um novo favorito")

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

    favorito_doc = {
        "produto": {
            "id": produto["_id"],
            "nome": produto["nome"],
            "preco_unitario": produto["preco_unitario"]
        },
        "vendedor": {
            "id": produto["vendedor"]["_id"],
            "nome": produto["vendedor"]["nome"]
        },
        "usuario": {
            "id": usuario["_id"],
            "nome": usuario["nome"]
        }
    }

    x = mycol.insert_one(favorito_doc)
    print("Favorito inserido com ID", x.inserted_id)


def read_favorito(nome_usuario=""):
    global db
    mycol = db.favorito
    print("\nFavoritos:")

    if nome_usuario:
        myquery = { "usuario.nome": nome_usuario }
        favoritos = mycol.find(myquery)
    else:
        favoritos = mycol.find()

    for fav in favoritos:
        print(f"ID: {fav['_id']}, Produto: {fav['produto']['nome']} - R${fav['produto']['preco_unitario']}, "
              f"Vendedor: {fav['vendedor']['nome']}, Usuário: {fav['usuario']['nome']}")


def update_favorito(fav_id):
    global db
    mycol = db.favorito
    fav = mycol.find_one({ "_id": ObjectId(fav_id) })

    if not fav:
        print("Favorito não encontrado.")
        return

    print("Favorito atual:", fav)

    produto_id = input("Mudar id do produto: ")
    if produto_id:
        produto = db.produto.find_one({ "_id": ObjectId(produto_id) })
        if not produto:
            print("Produto não encontrado.")
            return
        fav["produto"] = {
            "id": produto["_id"],
            "nome": produto["nome"],
            "preco_unitario": produto["preco_unitario"]
        }
        fav["vendedor"] = {
            "id": produto["vendedor"]["_id"],
            "nome": produto["vendedor"]["nome"]
        }

    usuario_id = input("Mudar id do usuário: ")
    if usuario_id:
        usuario = db.usuario.find_one({ "_id": ObjectId(usuario_id) })
        if not usuario:
            print("Usuário não encontrado.")
            return
        fav["usuario"] = {
            "id": usuario["_id"],
            "nome": usuario["nome"]
        }

    newvalues = { "$set": fav }
    mycol.update_one({ "_id": ObjectId(fav_id) }, newvalues)
    print("Favorito atualizado.")


def delete_favorito(fav_id):
    global db
    mycol = db.favorito
    mycol.delete_one({ "_id": ObjectId(fav_id) })
    print("Favorito deletado.")
