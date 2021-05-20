import requests

file = {'file':open('data.txt', 'rb')}

response= requests.post('https://gttb.guane.dev/api/files',files=file)
print(response.text)