﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Top n videos más vistos para determinado país y categoría")
    print("4- ")#TODO Requerimiento estudiante A
    print("5- Video que más días ha sido trending para una categoría")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        answer = controller.loadData(catalog)
        print("El total de videos cargados es: " + str(controller.videosSize(catalog)))
        print("El total de categorías cargadas es: " + str(controller.categoriesSize(catalog)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}"," || ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        
    
    elif int(inputs[0]) == 3:
        category = input("Sobre que catergoría desea buscar: ")
        country = input("Sobre que país desea buscar : ")
        rank = int(input("Ingrese la cantidad de videos para el top de vistas: "))
        """
        Se le pide al usuario el nombre de una categoria y se retorna el numero correspondiente

        Luego segun el pais indicado se busca la lista correspondiente a categoria+pais

        Finalmente se organizan los videos por numero de views

        """
        categoryNumber = (controller.getCategory(catalog,category.lower().strip()))
        categoryAndCountry = controller.getCategoryAndCountry(catalog, categoryNumber + country.lower().strip()) 
        answer = controller.sortVideosByViews(categoryAndCountry, rank)
        print("El top "+str(rank)+ " de videos con más views para la categoría "+category+" en el país ["+country+"] son: ")
        controller.printReqOne(answer, rank)
    
    elif int(inputs[0]) == 4:
        #TODO Requerimiento estudiante A
        pass

    elif int(inputs[0]) == 5:
        category = input("Sobre que catergoría desea buscar: ")

    else:
        sys.exit(0)
sys.exit(0)
