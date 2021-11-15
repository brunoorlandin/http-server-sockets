import json
import socket


def postData(params):
    result = {}
    filename = params[0].decode().split()[1]
    data = params[-1].decode().split("&")
    result['name'] = data[0].split("=")[1]
    result['password'] = data[1].split("=")[1]
    return result
