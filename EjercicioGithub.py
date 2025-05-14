import requests

username = 'torvalds'
url = f"https://api.github.com/users/{username}/repos"

response = requests.get(url)

if response.status_code == 200:
    repos = response.json()
    goodRepos = []

    # Filtrar repos con más de 100 estrellas
    for repo in repos:
        if repo['stargazers_count'] > 100:
            goodRepos.append(repo)

    # Ordenar por cantidad de estrellas (descendente)
    goodRepos.sort(key=lambda r: r['stargazers_count'], reverse=True)

    # Mostrar los primeros 5
    for good in goodRepos[:5]:
        print(f"Nombre: {good['name']} - Descripción: {good['description']} - ⭐ {good['stargazers_count']}")

else:
    print("Error al obtener datos: ", response.status_code)
