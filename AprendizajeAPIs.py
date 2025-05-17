import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print(response.status_code)

users = response.json()
"""
for i in range(5):
    texto = f"Nombre: {users[i]['name']}"
    if users[i]['website'].split('.')[1]== 'org': -> Esta funcion hace que realmente sea interesante mi código
        texto += f'Website: {users[i]['website']}'
    print(texto)
"""

for user in users[:10]:
    if user['website'].endswith('.org'):
        print(f"Nombre: {user['name']} - Website: {user['website']}")
        print(f"Ciudad: {user['address']['geo']['lng']}")