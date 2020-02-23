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
    return catalog




def newMovie (row):
    """
    Crea una nueva estructura para almacenar los actores de una pelicula 
    """
    movie = {"movies_id": row['id'], "title":row['title'], "average_rating":row['vote_average'], "ratings_count":row['vote_count']}
    return movie

def addMovieList (catalog, row):
    """
    Adiciona libro a la lista
    """
    movies = catalog['moviesList']
    movie = newMovie(row)
    lt.addLast(movies, movie)

def addMovieMap (catalog, row):
    """
    Adiciona libro al map con key=title
    """
    movies = catalog['moviesMap']
    movie = newMovie(row)
    map.put(movies, movie['title'], movie, compareByKey)

def addIdMap (catalog, row):
    """
    Adiciona libro al map con key=title
    """
    movies = catalog['idMap']
    movie = newMovie(row)
    map.put(movies, movie['id'], movie['vote_average'], compareByKey)

def newDirector (name, row):
    """
    Crea una nueva estructura para modelar un director y sus peliculas
    """
    director = {'name':"", "directorMovies":None,  "sum_average_rating":0}
    director ['name'] = name
    director['sum_average_rating'] = float(row['average_rating'])
    director ['directorMovies'] = lt.newList('SINGLE_LINKED')
    lt.addLast(director['directorMovies'],row['movies_id'])
    return director

def addDirector (catalog, name, row):
    """
    Adiciona un autor al map y sus libros
    """
    if name:
        directors = catalog['directors']
        director=map.get(directors,name,compareByKey)
        if director:
            lt.addLast(director['directorMovies'],row['movies_id'])
            director['sum_average_rating'] += float(row['average_rating'])
        else:
            director = newDirector(name, row)
            map.put(directors, director['name'], director, compareByKey)



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
    Retorna el autor a partir del nombre
    """
    return map.get(catalog['directors'], directorName, compareByKey)

def getPositiveVotes (catalog, directorName):
    director= getDirectorInfo(catalog, directorName)
    if director:
        movies=director['directorMovies']
        positivos=0
        for id in movies:
            vote=map.get(catalog['moviesMap'],id,compareByKey)
            if vote>=6:
                positivos+=1
        return positivos
    return None 

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByTitle(bookTitle, element):
    return  (bookTitle == element['title'] )
