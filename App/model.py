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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import arraylistiterator as alit
from DISClib.DataStructures import linkedlistiterator as slit
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# ========================
# Construccion de modelos
# ========================

def newCatalog ():
    """
    Crea una lista vacia para guardar todos los videos

    Se crean indices (MAPS) por los siguientes criterios:

    country
    category_id

    Retorna el catalogo iniciado
    """

    catalog = {'videos':None,
               'videosByCategory':None, # Laboratorio 6
               'categories':None,
               'categoriesAndCountries':None }
    
    catalog['videos'] = lt.newList(datastructure='SINGLE_LINKED')

    catalog['videosByCategory'] = mp.newMap(41,
                                      maptype='PROBING',
                                      loadfactor=0.5
                                      )

    catalog['categories'] = mp.newMap(41,
                                      maptype='PROBING',
                                      loadfactor=0.5
                                      )
    
    catalog['categoriesAndCountries'] = mp.newMap(500,
                                                  maptype='CHAINING',
                                                  loadfactor=0.5)
    
    catalog['videosById'] = mp.newMap(100000,
                             maptype='PROBING',
                             loadfactor=0.5
                             )

    catalog['countriesOrCategoriesById'] = mp.newMap(500,
                                                  maptype='CHAINING',
                                                  loadfactor=0.5)

    return catalog

# ===============================================                                      
# Funciones para agregar informacion al catalogo
# ===============================================

def addVideo(catalog, video):
    """
    Agrega el video a la lista de videos
    """
    lt.addLast(catalog['videos'], video)


def addVideoByCategory(catalog, video):
    existsCategory = mp.contains(catalog['videosByCategory'],video['category_id'])

    if existsCategory:
        existing = mp.get(catalog['videosByCategory'],video['category_id'])
        existingList = me.getValue(existing)
        lt.addLast(existingList, video)
    
    else:
        lists = lt.newList()
        lt.addFirst(lists, video)
        mp.put(catalog['videosByCategory'],video['category_id'],lists)


def addCategory(catalog, category):
    """
    Agrega la categoria al MAP usando el id como llave y el name como valor
    """
    mp.put(catalog['categories'],(category['name'].lower().strip()),category['id'])


def addCategoryAndCountry(catalog, video):
    """
    
    """
    existsCategoryAndCountry = mp.contains(catalog['categoriesAndCountries'], (video['category_id'] + video['country'].lower().strip()))

    if existsCategoryAndCountry:
        existing = mp.get(catalog['categoriesAndCountries'],(video['category_id'] + video['country'].lower().strip()) )
        existingList = me.getValue(existing)
        lt.addLast(existingList, video)
    
    else:
        lists = lt.newList('ARRAY_LIST')
        lt.addFirst(lists, video)
        mp.put(catalog['categoriesAndCountries'],(video['category_id'] + video['country'].lower().strip()), lists)


def addVideoById(catalog,video):

    existingVideoId = mp.contains(catalog['videosById'],video['video_id'])

    if existingVideoId:
        exists = mp.get(catalog['videosById'],video['video_id'])
        me.getValue(exists)['trending_time']+=1
        
    else:
        mp.put(catalog['videosById'],video['video_id'],video)

# =================================
# Funciones para creacion de datos
# =================================

def createList(catalog):
    trendingList = mp.valueSet(catalog['videosById'])
    
    return trendingList

def createMap(catalog, idList):

    iterator = slit.newIterator(idList)

    while slit.hasNext(iterator):

        video = slit.next(iterator)
        """
        Categorizacion por categorias
        """
        existingCategory = mp.contains(catalog['countriesOrCategoriesById'],video['category_id'])

        if existingCategory:
            existsCategory = mp.get(catalog['countriesOrCategoriesById'],video['category_id'])
            categoryList = me.getValue(existsCategory)
            lt.addLast(categoryList, video)

        else: 
            newCategoryList = lt.newList('ARRAY_LIST')
            lt.addFirst(newCategoryList, video)
            mp.put(catalog['countriesOrCategoriesById'],video['category_id'],newCategoryList)

        """
        Categorizacion por paises
        """
        existingCountry = mp.contains(catalog['countriesOrCategoriesById'],video['country'])

        if existingCountry:
            existsCountry = mp.get(catalog['countriesOrCategoriesById'],video['country'])
            countryList = me.getValue(existsCountry)
            lt.addLast(countryList, video)

        else: 
            newCountryList = lt.newList('ARRAY_LIST')
            lt.addFirst(newCountryList, video)
            mp.put(catalog['countriesOrCategoriesById'],video['country'],newCountryList)


# ======================
# Funciones de consulta
# ======================

def videosSize(catalog):
    return lt.size(catalog['videos'])

def categoriesSize(catalog):
    return mp.size(catalog['categories'])

def getCategory(catalog, category_name):
    category = mp.get(catalog['categories'],category_name)
    
    return category['value']

def getCategoryAndCountry(catalog, categoryAndCountry):
    catAndCounList = mp.get(catalog['categoriesAndCountries'],categoryAndCountry)
    answer = catAndCounList['value']

    return answer

def getCountryOrCategory(catalog, category):
    categoryKeyValue = mp.get(catalog['countriesOrCategoriesById'], category)
    categoryList = me.getValue(categoryKeyValue)

    return categoryList


# =================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# =================================================================

def compareViews(video1, video2):
    """
    Compara el numero de views de dos videos, devuelve verdadero si el primero es mayor que el segundo
    """
    return int(video1['views']) > int(video2['views'])

def compareTrending(video1, video2):
    """
    Compara el tiempo de trendig de dos videos, devuelve verdadero si el primero es mayor que el segundo
    """
    return int(video1['trending_time']) > int(video2['trending_time'])

# ==========================
# Funciones de ordenamiento
# ==========================

def sortVideosByViews(categoryAndCountry, rank):

    sortedList = sa.sort(categoryAndCountry, compareViews)
    subList = lt.subList(sortedList,1,rank)

    return subList

def sortVideosByTrending(categoryList, rank):

    sortedList = sa.sort(categoryList, compareTrending)
    subList = lt.subList(sortedList,1,rank)

    return subList
    

# =========================
# Funciones de comparación
# =========================

def compareVideoIds(id1, id2):
    """
    Compara dos ids de dos libros
    """
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def compareMapVideoIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id)==int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

# ================================
# Funciones para imprimir valores
# ================================

def printReqOne(orderedList,rank):

    iterator = alit.newIterator(orderedList)
    counter = 1
    print("trending_date\ttitle\tchannel_title\tpublish_time\tviews\tlikes\tdislikes")

    while alit.hasNext(iterator):

        element = alit.next(iterator)
        print("["+str(counter)+"] " +
              element['trending_date'] + "\t" +
              element['title'] + "\t" +
              element['channel_title'] + "\t" +
              element['publish_time'] + "\t" +
              element['views'] + "\t" +
              element['likes'] + "\t" +
              element['dislikes']
              )
        counter += 1

def printReqThree(oneVideoList):
    video = lt.firstElement(oneVideoList)
    print("title\tchannel_title\tcategory_id\ttrending_time")
    print(video['title'] + "\t" +
          video['channel_title'] + "\t" +
          video['category_id']+ "\t" +
          str(video['trending_time']))
