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
    """
    loadVideos(catalog)
    loadCategories(catalog)

def loadVideos(catalog):
    """
    Carga los videos del archivo. Por cada video se indica al modelo que debe adicionarlo al catalogo
    """
    videosfile = cf.data_dir + 'Samples/videos-5pct.csv'
    inputfile = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in inputfile:
        model.addVideo(catalog, video)
        model.addCategoryAndCountry(catalog, video)

def loadCategories(catalog):
    """
    Carga todas las categorias del archivo e indica al modelo que los adicione al catalogo
    """
    categoriesfile = cf.data_dir + 'Samples/category-id.csv'
    inputfile = csv.DictReader(open(categoriesfile, encoding='utf-8'))
    for category in inputfile:
        model.addCategory(catalog, category)


# Funciones de ordenamiento


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