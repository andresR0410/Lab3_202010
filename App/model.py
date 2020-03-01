"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import map as map
from DataStructures import listiterator as it


"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de peliculas. Retorna el catalogo inicializado.
    """
    catalog = {'moviesList':None, 'directors':None, 'moviesMap': None, 'actors': None}
    catalog['moviesList'] = lt.newList("ARRAY_LIST")
    catalog['moviesMap'] = map.newMap (100003, maptype='CHAINING') #peliculas 329044
    catalog['idMap'] = map.newMap (100003, maptype='CHAINING')
    catalog['directors'] = map.newMap (171863, maptype='PROBING') #directores 85929
    catalog['actors'] = map.newMap (86959, maptype='CHAINING') #actores 260861
    catalog['genres']=map.newMap(100003, maptype='CHAINING' ) #no sé cuantos géneros hay TOCA CAMBIARLO DESPUES
    return catalog




def newMovie (row):
    """
    Crea una nueva estructura para almacenar los datos de una pelicula 
    """
    movie = {"movies_id": row['id'], "title":row['original_title'], "vote_average":row['vote_average'], "vote_count":row['vote_count']}
    return movie

def addMovieList (catalog, row):
    """
    Adiciona película a la lista
    """
    movies = catalog['moviesList']
    movie = newMovie(row)
    lt.addLast(movies, movie)

def addMovieMap (catalog, row):
    """
    Adiciona película al map con key=title
    """
    movies = catalog['moviesMap']
    movie = newMovie(row)
    map.put(movies, movie['title'], movie, compareByKey)

def addIdMap (catalog, row):
    """
    Adiciona película al map con key=id
    """
    movies = catalog['idMap']
    movie = newMovie(row)
    map.put(movies, movie['movies_id'], movie, compareByKey)

def newGenre (row):
    """
    Crea una nueva estructura para almacenar los datos por género
    """
    genre = {"name": " ", "movies": lt.newList(), "sum_average_rating": 0}
    genre['name']=row['genre']
    lt.addLast(genre['movies'],row['id'])
    genre['sum_average_rating']= float(row['vote_average'])

    return genre

def addGenre(catalog, row):
    """
    Adiciona el género al mapa con key=genre
    """
    genres=catalog['genres']
    id=row['id']
    vote=row['vote_average']
    genre= map.get(genres, row['genre'], compareByKey)
    if genre:
        lt.addLast(genre['movies'], id)
        genre['sum_average_rating'] += float(vote)
    else:
        genre = newGenre(row)
        map.put(genres, genre['name'], genre, compareByKey)

def newDirector (row, average, movieTitle):
    """
    Crea una nueva estructura para modelar un director y sus peliculas
    """
    director = {'name':"", "directorMovies":lt.newList(),  "sum_average_rating":0}
    director ['name'] = row['director_name']
    director['sum_average_rating'] = average
    lt.addLast(director['directorMovies'],movieTitle)
    return director

def updateDirector (director, average, movieTitle):
    director['sum_average']+=average
    lt.addLast(director['directorMovies'], movieTitle)

def addDirector (catalog, row):
    """
    Adiciona un director al mapa
    """
    movies=catalog['idMap']
    directors = catalog['directors']
    id= row['id']
    movie=map.get(movies, id, compareByKey)
    average=float(movie['vote_average'])
    movieTitle=movie['title']
    director=map.get(directors,row['director_name'],compareByKey)
    if director:
        updateDirector(director, average, movieTitle)
    else:
        director = newDirector(row, average, movieTitle)
        map.put(directors, director['name'], director, compareByKey)

def newActor (actorName, movie, director, vote):
    """
    Crea una nueva estructura para modelar un actor y sus peliculas
    """
    actor = {'name':"", "movies":None,  "sum_average_rating":0, "director": ""}
    actor ['name'] = actorName
    actor['sum_average_rating'] = float(vote)
    actor ['movies'] = lt.newList()
    lt.addLast(actor ['movies'], movie)
    actor ['director']= director
    return actor

def updateActor (actor, vote, movie, director):
    pass

def addActor (catalog, row):
    pass



# Funciones de consulta


def getMovieInList (catalog, movieTitle):
    """
    Retorna el libro desde la lista a partir del titulo
    """
    pos = lt.isPresent(catalog['moviesList'], movieTitle, compareByTitle)
    if pos:
        return lt.getElement(catalog['moviesList'],pos)
    return None


def getMovieInMap (catalog, movieTitle):
    """
    Retorna la película desde el mapa a partir del titulo (key)
    """
    return map.get(catalog['moviesMap'], movieTitle, compareByKey)


def getDirectorInfo (catalog, directorName):
    """
    Retorna el director a partir del nombre
    """
    return map.get(catalog['directors'], directorName, compareByKey)

def getActorInfo (catalog, actorName):
    """
    Retorna el actor a partir del nombre
    """
    return map.get(catalog['actors'], actorName, compareByKey)

def getGenreInfo (catalog, genreName):
    """
    Retorna información sobre el género a partir del nombre
    """
    return map.get(catalog['genres'], genreName, compareByKey)

def getPositiveVotes (catalog, directorName):
    director= getDirectorInfo(catalog, directorName)
    if director:
        movies=director['directorMovies']
        #print (type(movies))
        positivos=0
        size = lt.size(movies)
    
        if size:
            iterator = it.newIterator(movies)
            while  it.hasNext(iterator):
                id = it.next(iterator)
            #print(id)
            #print(type(id))
                vote=map.get(catalog['idMap'],id,compareByKey)
                if vote!=None:
                #print(vote)
                    if float(vote)>=6:
                        positivos+=1
        return positivos
    return None 

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(movieTitle, element):
    return  (movieTitle == element['title'] )
