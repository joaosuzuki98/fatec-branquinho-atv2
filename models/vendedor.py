from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_URL_LOCAL')

# Create a new client and connect to the server
client = MongoClient(uri)
global db
db = client.mercadolivre

def delete_usuario(email):
    #Delete
    global db
    mycol = db.vendedor
    myquery = {"email": email}
    mycol.delete_one(myquery)
    print("Deletado o vendedor ", email)

def create_vendedor():
    #Insert
    global db
    mycol = db.vendedor
    print("\nInserindo um novo vendedor")
    nome = input("Nome: ")
    email = input("Email: ")
    cpf = input("CPF: ")
    cnpj = input("CNPJ: ")
    senha = input("Senha: ")
    key = 1
    end = []
    while (key != 'N'):
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {        #isso nao eh json, isso é chave-valor, eh um obj
            "rua":rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco) #estou inserindo na lista
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = { "nome": nome, "email": email, "cpf": cpf, "cnpj": cnpj, "end": end, "senha": senha }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_vendedor(nome):
    #Read
    global db
    mycol = db.vendedor
    print("Vendedores existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(f"ID: {x["id"]}, Nome: {x["nome"]}, CPF/CNPJ: {x["cpf"] if x["cpf"] else x["cnpj"]}")
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_vendedor(email):
    #Read
    global db
    mycol = db.vendedor
    myquery = {"email": email}
    mydoc = mycol.find_one(myquery)
    print("Dados do vendedor: ",mydoc)
    nome = input("Mudar Nome: ")
    if len(nome):
        mydoc["nome"] = nome

    email = input("Mudar email: ")
    if len(email):
        mydoc["email"] = email

    cpf = input("Mudar CPF: ")
    if len(cpf):
        mydoc["cpf"] = cpf

    cnpj = input("Mudar CNPJ: ")
    if len(cnpj):
        mydoc["cnpj"] = cnpj

    senha = input("Mudar senha: ")
    if len(senha):
        mydoc["senha"] = senha

    for end in mydoc["end"]:
        rua = input("Mudar rua: ")
        if len(rua):
            end["rua"] = rua

        num = input("Mudar num: ")
        if len(num):
            end["num"] = num

        bairro = input("Mudar bairro: ")
        if len(bairro):
            end["bairro"] = bairro

        cidade = input("Mudar cidade: ")
        if len(cidade):
            end["cidade"] = cidade

        estado = input("Mudar estado: ")
        if len(estado):
            end["estado"] = estado

        cep = input("Mudar cep: ")
        if len(cep):
            end["cep"] = cep

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)
