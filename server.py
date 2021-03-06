from os import name
from scriptPost import postData
import socket
import json
import os

SERVER_HOST = ""

SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print("Servidor em execução...")
print("Acesse o link: http://localhost:%s" % SERVER_PORT)


def post(params):
    result = postData(params)

    try:
        response = "HTTP/1.1 200 OK\n\n" + \
            result['name'] + ":" + result['password']
    except FileNotFoundError:
        # caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
        response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"

    return response


def delete(headers):
    resource = headers[0].decode().split()[1]
    resourceFomated = resource.split("/")
    resourceFomated.pop(0)

    if len(resourceFomated) == 1:
        resourceString = resourceFomated[0]
    else:
        resourceString = ""
        for i in range(len(resourceFomated)):
            resourceString += "/"
            resourceString += resourceFomated[i]
        resourceString = resourceString[1:]

    if os.path.exists(resourceString):
        os.remove(resourceString)
        code = "HTTP/1.1 200 OK\n\n"
        isDeleted = "Recurso deletado"
    else:
        code = "HTTP/1.1 404 NOT FOUND\n\n"
        isDeleted = "Recurso nao encontrado"

    response = code + isDeleted

    return response


def put(headers, body):
    resource = headers[0].decode().split()[1]
    resourceFomated = resource.split("/")
    resourceFomated.pop(0)

    if len(resourceFomated) == 1:
        resourceString = resourceFomated[0]
    else:
        resourceString = ""
        for i in range(len(resourceFomated)):
            resourceString += "/"
            resourceString += resourceFomated[i]
        resourceString = resourceString[1:]

    content = body[-1]

    try:
        file = open(resourceString, "wb")
        file.write(content)
        file.close()
        response = "HTTP/1.1 200 OK\n\nRecurso recebido"
    except:
        response = "HTTP/1.1 404 NOT FOUND\n\nRecurso nao recebido"

    return response


def get(headers):
    filename = headers[0].decode().split()[1]

    # verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
    if filename == "/":
        filename = "/index.html"

    # try e except para tratamento de erro quando um arquivo solicitado não existir
    try:
        # abrir o arquivo e enviar para o cliente
        fin = open("htdocs" + filename)
        # leio o conteúdo do arquivo para uma variável
        content = fin.read()
        # fecho o arquivo
        fin.close()
        # envia a resposta
        response = "HTTP/1.1 200 OK\n\n" + content
    except FileNotFoundError:
        # caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
        response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"

    return response


while True:

    # espera por conexões
    # client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    # client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    # pega a solicitação do cliente
    request = bytes()
    request_chunk = client_connection.recv(2048)
    client_connection.settimeout(1)
    try:
        while request_chunk:
            request += request_chunk
            request_chunk = client_connection.recv(2048)
    except:
        pass

    client_connection.settimeout(0)

    # verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        headers = request.split("\n".encode())
        body = request.split("\r\n\r\n".encode())

        # verifica qual tipo de requisicao
        requestType = headers[0].decode().split("/")[0].lower().strip()

        try:
            if requestType == "get":
                res = get(headers)
            elif requestType == "put":
                res = put(headers, body)
            elif requestType == "post":
                res = post(headers)
            elif requestType == "delete":
                res = delete(headers)
            else:
                res = "HTTP/1.1 404 METHOD NOT FOUND\n\n"
        except FileNotFoundError:
            # caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
            response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"

        # envia a resposta HTTP
        client_connection.sendall(res.encode())

        client_connection.close()

server_socket.close()
