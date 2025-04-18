from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_URL_LOCAL')

# Create a new client and connect to the server
client = MongoClient(uri)
global db
db = client.mercadolivre

def delete_produto(prod_id):
    #Delete
    global db
    mycol = db.produto
    myquery = {"id": prod_id}
    mycol.delete_one(myquery)
    print("Deletado o produto ", prod_id)

def create_produto():
    #Insert
    global db
    mycol = db.produto
    print("\nInserindo um novo produto")
    nome = input("Nome: ")
    preco_unitario = input("Preço unitário: ")
    vend_id = input("ID do vendedor: ")
    vend = db.vendedor.find_one({ "id": vend_id })
    vendedor = { "id": vend["id"], "nome": vend["nome"], "email": vend["email"] }
    mydoc = { "nome": nome, "preco_unitario": preco_unitario, "vendedor": vendedor }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_produto(nome):
    #Read
    global db
    mycol = db.produto
    print("Produtos existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(f"ID: {x["id"]}, Nome: {x["nome"]}, preço unitário: {x["preco_unitario"]}")
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_produto(nome):
    #Read
    global db
    mycol = db.produto
    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do produto: ",mydoc)
    nome = input("Mudar Nome: ")
    if len(nome):
        mydoc["nome"] = nome

    preco_unitario = input("Mudar preço unitário: ")
    if len(preco_unitario):
        mydoc["preco_unitario"] = preco_unitario

    vend_id = input("Mudar id do vendedor: ")
    if len(vend_id):
        mydoc["vendedor"]["id"] = vend_id

    vend = db.vendedor.find_one({ "id": vend_id })
    vendedor = { "id": vend["id"], "nome": vend["nome"], "email": vend["email"] }

    mydoc["vendedor"] = vendedor

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
