"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# ======================================
# Inicialización del Catálogo de libros
# ======================================

def initCatalog():
    """
    Llama a la función de creación del catalogo
    """
    catalog = model.newCatalog()
    return catalog

# =================================
# Funciones para la carga de datos
# =================================

def loadData(catalog):
    """
    Cargar los datos del archivo y cargarlos en la estructura de datos
    Y calcula el tiempo y la memoría
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadVideos(catalog)
    loadCategories(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadVideos(catalog):
    """
    Carga los videos del archivo. Por cada video se indica al modelo que debe adicionarlo al catalogo
    """
    videosfile = cf.data_dir + 'Samples/videos-30pct.csv' #TODO cambiar la cantidad de videos por cargar
    inputfile = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in inputfile:
        model.addVideo(catalog, video)
        model.addVideoByCategory(catalog,video)
        model.addCategoryAndCountry(catalog, video)

def loadCategories(catalog):
    """
    Carga todas las categorias del archivo e indica al modelo que los adicione al catalogo
    """
    categoriesfile = cf.data_dir + 'Samples/category-id.csv'
    inputfile = csv.DictReader(open(categoriesfile, encoding='utf-8'))
    for category in inputfile:
        model.addCategory(catalog, category)

# ==========================
# Funciones de ordenamiento
# ==========================

def sortVideosByViews(categoryAndCountry, rank):
    return model.sortVideosByViews(categoryAndCountry, rank)


# ========================================
# Funciones de consulta sobre el catálogo
# ========================================

def videosSize(catalog):
    return model.videosSize(catalog)

def categoriesSize(catalog):
    return model.categoriesSize(catalog)

def getCategory(catalog,category):
    return model.getCategory(catalog,category)

def getCategoryAndCountry(catalog, categoryAndCountry):
    return model.getCategoryAndCountry(catalog, categoryAndCountry)

# ======================================
# Funciones para medir tiempo y memoria
# ======================================

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes
    """

    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte a kByte
    delta_memory /= 1024.0
    return delta_memory
