import json
import requests
import re


def carregar_ocorrencia(ocorrencia):
    r = requests.post("http://webserver-nao-vacila.herokuapp.com/ocorrencia/",
                      data=ocorrencia)
    return r


def gerar_ocorrencia(data):
    ocorrencia = {}
    ocorrencia['id_tipo'] = data['id_tipo']
    ocorrencia['descricao'] = data['sub-titulo']
    ocorrencia['latitude'] = data['latitude']
    ocorrencia['longitude'] = data['longitude']
    ocorrencia['hora'] = data['hora']
    ocorrencia['endereco'] = data['endereco']
    ocorrencia['data'] = data['data']
    ocorrencia['titulo'] = data['titulo']
    return ocorrencia


contagem_endereco = 0
contagem_ocorrencia_com_endereco = 0
with open('backup/data.txt') as json_data:
    dados = json.load(json_data)
    for count, noticia in enumerate(dados):
        print(count)
        rua_regex = re.search('rua (\w|\s)+', noticia['texto'])
        avenida_regex = re.search('avenida (\w|\s)+', noticia['texto'])
        avenida = None
        rua = None
        existe_endereco = False
        if rua_regex:
            contagem_endereco += 1
            rua = rua_regex.group()
            existe_endereco = True
        if avenida_regex:
            contagem_endereco += 1
            avenida = avenida_regex.group()
            existe_endereco = True
        texto = ''
        texto += noticia['titulo']
        texto += noticia['sub-titulo']
        texto += noticia['tag']
        texto += noticia['texto']
        if existe_endereco:
            endereco = {}
            response = None
            if rua:
                response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+rua)
            elif avenida:
                response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+avenida)
            endereco_encontradao = False
            if response:
                for each in response.json()['results']:
                    if 'PE' in each['formatted_address']:
                        noticia['longitude'] = each['geometry']['location']['lng']
                        noticia['latitude'] = each['geometry']['location']['lat']
                        noticia['endereco'] = each['formatted_address']
                        endereco_encontradao = True
                interesse = False
                if 'roubo' in texto or 'rouba' in texto or 'furt' in texto:
                    noticia['id_tipo'] = 2
                    interesse = True
                elif 'assalt' in texto:
                    noticia['id_tipo'] = 1
                    interesse = True
                elif 'homicidio' in texto or 'assassinad' in texto or 'matar' in texto or \
                    'morre' in texto or 'mort' in texto:
                    noticia['id_tipo'] = 6
                    interesse = True
                elif 'arromba' in texto:
                    noticia['id_tipo'] = 4
                    interesse = True
                elif 'sequestr' in texto:
                    noticia['id_tipo'] = 3
                    interesse = True
                elif 'tiro' in texto:
                    noticia['id_tipo'] = 5
                    interesse = True
                elif 'droga' in texto:
                    noticia['id_tipo'] = 7
                    interesse = True
                if interesse and endereco_encontradao:
                    contagem_ocorrencia_com_endereco += 1
                    ocorrencia = gerar_ocorrencia(noticia)
                    carregar_ocorrencia(ocorrencia)

print(contagem_endereco)
print(contagem_ocorrencia_com_endereco)
# rua alto treze de maio
# 1 assalto
# 2 roubo
# 3 sequestro
# 4 arrombamento
# 5 tiroteio
# 6 homicidio
# 7 trafico
