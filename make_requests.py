import requests

url = 'http://0.0.0.0:8001/repostajes/add'

data = {
    'estacion': 2,
    'usuario': 'eva',
    'matricula': '12HWS',
    'combustible': 'sin plomo 95',
    'litros': '25.00',
    'albaran': '3123ADAG',
}

print requests.post(url, data=data)
