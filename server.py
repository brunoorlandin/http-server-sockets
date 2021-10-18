import socket

SERVER_HOST = ""

SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print("Servidor em execução...")
print("Acesse o link: http://localhost:%s" % SERVER_PORT)


def post(params):
    print(params[-1])
    filename = headers[0].split()[1]
    print(filename)
    return 'headers[0].split()[1]'


def delete():
    print("delete")


def put():
    print("put")


def get(headers):
    filename = headers[0].split()[1]
    print(filename)

    # verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
    if filename == "/":
        filename = "/index.html"

    if filename == "/register.html":
        filename = "/register.html"

    if filename == "/ipsum.html":
        filename = "/ipsum.html"

    if filename == "/utils/icons8-group-task-96.png":
        filename = "/utils/icons8-group-task-96.png"

    if filename == "/index.css":
        filename = "/index.css"

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
    request = client_connection.recv(1024).decode()
    # verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        # print(request)

        headers = request.split("\n")

        # verifica qual tipo de requisicao
        requestType = headers[0].split("/")[0].lower().strip()
        #print(f'headers => {headers}')
        print(f'req type => {requestType}')
        if requestType == "get":
            print("Recebeu GET")
            res = get(headers)
        elif requestType == "put":
            print("Recebeu put")
        elif requestType == "post":
            print("Recebeu post")
            res = post(headers)
        elif requestType == "delete":
            print("Recebeu delete")
        else:
            print("recebeu um metodo nao existente")
            res = "HTTP/1.1 404 METHOD NOT FOUND\n\n"

        # envia a resposta HTTP
        client_connection.sendall(res.encode())

        client_connection.close()

server_socket.close()
