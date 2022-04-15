import requests

'''
a) En cuantas peliculas aparecen planetas cuyo clima sea arido?
b) Cuantos wookies aparecen en la sexta pelicula?
c) Cual es el nombre de la aeronave mas grande en toda la saga?
'''

def get_all(url):
    items = []
    next = True
    while next:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            json = response.json()
            for e in json['results']:
                items.append(e)
            if bool(json['next']):
                url = json['next']
            else:
                next = False
    return items

def starships_length(s):
    return float(s['length'].replace(",", ""))

def get_people_by_film(url):
    people = []
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        json = response.json()
        for c in json['characters']:
            cResponse = requests.get(c)
            if cResponse.status_code == requests.codes.ok:
                cJson = cResponse.json()
                people.append(cJson)
    return people

'''a) En cuantas peliculas aparecen planetas cuyo clima sea arido?'''
url = 'https://swapi.dev/api/planets/'
planets = get_all(url)
aPeliculas = []
for p in planets:
    if p['climate'] == 'arid' or p['climate'].find('arid'):
        for f in p['films']:
            numero = int(f[len(f) - 2])
            try:
                i = aPeliculas.index(numero)
            except ValueError as ve:
                aPeliculas.append(int(numero))
print("En cuantas peliculas aparecen planetas cuyo clima sea arido?: En " + str(len(aPeliculas)) + " peliculas")

'''b) Cuantos wookies aparecen en la sexta pelicula?'''
url = 'https://swapi.dev/api/films/6'
people = get_people_by_film(url)
wookies = 0
for p in people:
    for s in p['species']:
        response = requests.get(s)
        if response.status_code == requests.codes.ok:
            json = response.json()
            if json['name'] == 'Wookie':
                wookies = wookies + 1
print("Cuantos wookies aparecen en la sexta pelicula?: " + str(wookies) + " wookies")

'''c) Cual es el nombre de la aeronave mas grande en toda la saga?'''
url = 'https://swapi.dev/api/starships/'
starships = get_all(url)
starships.sort(reverse=True, key=starships_length)
print("Cual es el nombre de la aeronave mas grande en toda la saga?: " + starships[0]['name'] + "(" + starships[0]['length'] + " metros)")
