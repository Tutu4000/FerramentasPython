import requests
import re

def get_format(url):
    match = re.search("format=(\w+)", url)
    if match:
        return match.group(1)
    else:
        return None

def download(url): #
    request = requests.get(url)
    arquivo_nome = url.split("/")[-1]
    formato_php = get_format(arquivo_nome)
    if formato_php:
        nome_arquivo_criado = "downloaded." + formato_php
        with open(nome_arquivo_criado, "wb") as arquivo:
            arquivo.write(request.content)
    else:
        with open(arquivo_nome, "wb") as arquivo:
            arquivo.write(request.content)

download("https://pbs.twimg.com/media/CHkvBTbWoAMFIf3?format=jpg&name=medium")#Ignore a url teste





