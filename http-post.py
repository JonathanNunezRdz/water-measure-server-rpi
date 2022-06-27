import requests

url = 'http://192.168.1.73:4001/api/v1/distance'

distances = [3.4, 3.5, 3.44, 3.54, 3.42, 3.51, 3.44]

myjson = {
    'distances': distances,
    'id': 'rpi3b+'
}

res = requests.post(url, json=myjson)

print(res.text)