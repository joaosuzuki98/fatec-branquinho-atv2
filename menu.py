from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from models import vendedor, produto

load_dotenv()
uri = os.getenv('MONGODB_URL_LOCAL')

# Create a new client and connect to the server
client = MongoClient(uri)
global db
db = client.mercadolivre

def delete_usuario(email):
    #Delete
    global db
    mycol = db.usuario
    myquery = {"email": email}
    mycol.delete_one(myquery)
    print("Deletado o usuário ", email)

def create_usuario():
    #Insert
    global db
    mycol = db.usuario
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    email = input("Email: ")
    cpf = input("CPF: ")
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
    mydoc = { "nome": nome, "email": email, "cpf": cpf, "end": end, "senha": senha }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_usuario(nome):
    #Read
    global db
    mycol = db.usuario
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(f"ID: {x["id"]}, Nome: {x["nome"]}, CPF: {x["cpf"]}")
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def update_usuario(email):
    #Read
    global db
    mycol = db.usuario
    myquery = {"email": email}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome: ")
    if len(nome):
        mydoc["nome"] = nome

    email = input("Mudar email: ")
    if len(email):
        mydoc["email"] = email

    cpf = input("Mudar CPF: ")
    if len(cpf):
        mydoc["cpf"] = cpf

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

key = 0
sub = 0
while (key != 'S'):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    key = input("Digite a opção desejada? (S para sair) ")

    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("3-Update Usuário")
        print("4-Delete Usuário")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create usuario")
            create_usuario()
            
        elif (sub == '2'):
            nome = input("Read usuário, deseja algum usuário especifico? Digite o nome se sim: ")
            read_usuario(nome)
        
        elif (sub == '3'):
            email = input("Update usuário, deseja algum usuário específico? Digite o email se sim: ")
            update_usuario(email)

        elif (sub == '4'):
            print("delete usuario")
            email = input("Email do usuário a ser deletado: ")
            delete_usuario(email)
            
    elif (key == '2'):
        print("Menu do Vendedor")
        print("1-Create vendedor")
        print("2-Read vendedor")
        print("3-Update vendedor")
        print("4-Delete vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if sub == '1':
            print("Create vendedor")
            vendedor.create_vendedor()

        elif sub == '2':
            nome = input("Read vendedor, deseja algum vendedor específico? Digite o nome se sim: ")
            vendedor.read_vendedor(nome)

        elif sub == '3':
            email = input("Update vendedor, deseja algum vendedor específico? Digite o email se sim: ")
            vendedor.update_vendedor(email)

        elif sub == '4':
            print("delete vendedor")
            email = input("Email do vendedor a ser deletado: ")
            vendedor.delete_usuario(email)

    elif (key == '3'):
        print("Menu do produto")
        print("1-Create produto")
        print("2-Read produto")
        print("3-Update produto")
        print("4-Delete produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if sub == '1':
            print("Create produto")
            produto.create_produto()

        elif sub == '2':
            nome = input("Read produot, deseja algum produto específico? Digite o nome se sim: ")
            produto.read_produto(nome)

        elif sub == '3':
            nome = input("Update produto, deseja algum produto específico? Digite o nome se sim: ")
            produto.update_produto(nome)

        elif sub == '4':
            print("delete produto")
            prod_id = input("ID do produto a ser deletado: ")
            produto.delete_produto(prod_id)
      

print("Tchau Prof...")
