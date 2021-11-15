import json
import socket


def postData(params):
    result = {}
    filename = params[0].decode().split()[1]
    data = params[-1].decode().split("&")
    result['name'] = data[0].split("=")[1]
    result['password'] = data[1].split("=")[1]
    print(params)
    return result


# def postFile(name, password):
#file = open("htdocs/data.json", "a")
#json.dump(f'{name}:{password}', file)
#content = json.loads(file)
# print(content)
# file.close()
