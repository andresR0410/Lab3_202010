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
import model
import csv
from ADT import list as lt
from ADT import map as map

from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)



def compareratings (movie1, movie2):
    return ( float(movie1['vote_average']) > float(movie2['vote_average']))


# Funciones para la carga de datos 

def loadMovies (catalog, sep=';'):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    moviesfile = cf.data_dir + 'SmallMoviesDetailsCleaned.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(moviesfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona la pelócula a la lista de películas
            model.addMovieList(catalog, row)
            # Se adiciona la película al mapa de películas (key=title)
            model.addMovieMap(catalog, row)
            # Se adiciona el id de la pelicula al mapa de ids (key= id)
            model.addIdMap(catalog, row)
            # Se adiciona el género al mapa de géneros (key= genre)
            model.addGenre(catalog, row)

            
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga películas:",t1_stop-t1_start," segundos")   


def loadCasting(catalog):
    """
    Carga todos los directores
    """
    t1_start = process_time() #tiempo inicial
    castingfile = cf.data_dir + 'MoviesCastingRaw-small.csv'
    
    dialect = csv.excel()
    dialect.delimiter=";"
    with open(castingfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            model.addDirector (catalog, row)#cargar los directores
            model.addActor (catalog, row)#cargar los actores
            model.directorToId(catalog, row)#adicionar el director al mapa de ids
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga directores",t1_stop-t1_start," segundos")
    
def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadMovies(catalog)
    loadCasting(catalog)
    

# Funciones llamadas desde la vista y enviadas al modelo


def getMovieInfo(catalog, movieTitle):
    
    #movie=model.getMovieInList(catalog, movieTitle)
    movie=model.getMovieInMap(catalog, movieTitle)
    if movie:
        id=movie['movies_id']
        director=model.getDirectorById(catalog, id)
        print('La película', movie['title'], 'tiene un total de', movie['vote_count'], 'votos.')
        print('Tiene', movie['vote_average'], 'de voto promedio')
        print('Fue dirigida por', director)
        found='yes'
    else:
        found='no'
    return found

def getDirectorInfo(catalog, directorName):
    t1_start = process_time() #tiempo inicial
    director=model.getDirectorInfo(catalog, directorName)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución:",t1_stop-t1_start," segundos")   
    if director:
        return director
    else:
        return None  

def getActorInfo(catalog, actorName):
    t1_start = process_time() #tiempo inicial
    actor=model.getActorInfo(catalog, actorName)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución:",t1_stop-t1_start," segundos")   
    if actor:
        return actor
    else:
        return None  

def getGenreInfo (catalog, genreName):
    t1_start = process_time() #tiempo inicial
    genre=model.getGenreInfo(catalog, genreName)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución:",t1_stop-t1_start," segundos")   
    if genre:
        return genre
    else:
        return None 

def getPositiveVotes (catalog, directorName):
    t1_start = process_time() #tiempo inicial
    positives= model.getPositiveVotes(catalog, directorName)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución:",t1_stop-t1_start," segundos")
    return positives  

