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
import sys
import controller 
import csv
from ADT import list as lt
from ADT import map as map
from time import process_time 

from DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Laboratorio 3")
    print("1- Cargar información")
    print("2- Buscar película por titulo") #requerimiento 2
    print("3- Buscar información de director por nombre ...") #requrimiento 3
    print("4- Buscar películas con votación positiva dado un director") #requerimiento 1
    print("5- Buscar películas por actor") #requerimiento 4
    print("6- Buscar películas por género") #requerimiento 5
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo de peliculas
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga las peliculas en la estructura de datos
    """
    controller.loadData(catalog)


"""
Menu principal
"""
while True:
    printMenu()
    inputs =input('Seleccione una opción para continuar\n')
    if int(inputs[0])==1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog ()
        loadData (catalog)
        print ('Mapa Peliculas cargadas: ' + str(map.size(catalog['moviesMap'])))
        print ('Lista Peliculas cargadas: ' + str(lt.size(catalog['moviesList'])))
        print ('Directores cargados: ' + str(map.size(catalog['directors'])))
        print ('Mapa ids cargados:' + str(map.size(catalog['idMap'])))
        print ('Mapa géneros cargados:' + str(map.size(catalog['genres'])))
        
    elif int(inputs[0])==2:
        movieTitle = input("Nombre de la película a buscar: ")
        t1_start = process_time() #tiempo inicial
        found= controller.getMovieInfo (catalog, movieTitle)
        if found=='no':
            print("Película no encontrada")    
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución:",t1_stop-t1_start," segundos")   

    elif int(inputs[0])==3:
        directorName = input("Nombre del director que desea consultar: ")
        director = controller.getDirectorInfo (catalog, directorName)   
        if director:
            print("Peliculas del director",directorName,":",lt.size(director['directorMovies']))
            print("Lista de películas que ha dirigido:", director['directorMovies'])
            print("Promedio de Votacion",directorName,":",(director['sum_average_rating']/lt.size(director['directorMovies'])))
        else:
            print("Director no encontrado")

    elif int(inputs[0])==4:
        directorName = input ("Nombre del director a buscar: ")
        positives= controller.getPositiveVotes(catalog, directorName)
        if positives!=None:
            print ("EL director buscado tiene", positives,  "películas con votación positiva")
        else:
            print ('Director no encontrado')

    elif int(inputs[0])==5:
        actorName= input("Nombre del actor que dessea consultar: ")
        actor = controller.getActorInfo (catalog, actorName)
        if actor:
            print("Actor", actorName,":", lt.size(actor['movies']), "películas")
            print("Lista de películas:", actor['movies'])
            print("Promedio de Votacion:",(actor['sum_average_rating']/lt.size(actor['movies'])))
            print("EL director que más veces lo ha dirigido:", actor['director'])
        else:
            print("Actor no encontrado")

    elif int(inputs[0])==6:
        genreName = input("Ingrese el género que desea consultar: ")
        genre = controller.getGenreInfo (catalog, genreName)
        if genre:
            print("Género", genreName,":", lt.size(genre['movies']), "películas")
            print("Promedio de Votacion",genreName,":",(genre['sum_average_rating']/lt.size(genre['movies'])))
        else:
            print("Género no encontrado")

    else:
        sys.exit(0)
sys.exit(0)