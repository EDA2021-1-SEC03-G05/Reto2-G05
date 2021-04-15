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


from DISClib.DataStructures.arraylist import newList
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
                                                  loadfactor=4.0)
    
    catalog['videosById'] = mp.newMap(100000,
                             maptype='PROBING',
                             loadfactor=0.5
                             )

    catalog['CategoriesById'] = mp.newMap(41,
                                maptype='CHAINING',
                                loadfactor=4.0)

    catalog['videosByCountry'] =mp.newMap(100,
                                maptype='CHAINING',
                                loadfactor=4.0)

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
    Para el req 1, en un mapa añade llaves que son la union de una categoria y un pais y como valor guarda una lista de videos
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

def addVideoByCountry(catalog, video):

    existingCountry = mp.contains(catalog['videosByCountry'],video['country'])

    if existingCountry:
        exists = mp.get(catalog['videosByCountry'],video['country'])
        existingList = me.getValue(exists)
        lt.addLast(existingList,video)

    else: 
        list = lt.newList(datastructure='ARRAY_LIST')
        lt.addFirst(list, video)
        mp.put(catalog['videosByCountry'],video['country'],list)


# =================================
# Funciones para creacion de datos
# =================================

def createCategoryList(catalog):
    trendingList = mp.valueSet(catalog['videosById'])
    
    return trendingList

def createCategoryMap(catalog, idList):

    iterator = slit.newIterator(idList)

    while slit.hasNext(iterator):

        video = slit.next(iterator)
        """
        Categorizacion por categorias
        """
        existingCategory = mp.contains(catalog['CategoriesById'],video['category_id'])

        if existingCategory:
            existsCategory = mp.get(catalog['CategoriesById'],video['category_id'])
            categoryList = me.getValue(existsCategory)
            lt.addLast(categoryList, video)

        else: 
            newCategoryList = lt.newList('ARRAY_LIST')
            lt.addFirst(newCategoryList, video)
            mp.put(catalog['CategoriesById'],video['category_id'],newCategoryList)

def createUniqueCountry(list):

    idMap = mp.newMap(5500,
                      maptype='CHAINING',
                      loadfactor= 4.0)
    
    iterator = alit.newIterator(list)
    while alit.hasNext(iterator):
        video = alit.next(iterator)
        newLikes = video['likes']

        existingId = mp.get(idMap,video['video_id'])

        if existingId:
            keyValueId = mp.get(idMap,video['video_id'])
            existingVideo = me.getValue(keyValueId)
            if newLikes > existingVideo['likes']:
                existingVideo['likes']=newLikes

        else: 
            mp.put(idMap, video['video_id'],video)

    return mp.valueSet(idMap)



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

def getVideosByCategory(catalog, category):
    categoryKeyValue = mp.get(catalog['CategoriesById'], category)
    categoryList = me.getValue(categoryKeyValue)

    return categoryList

def getVideosByCountry(catalog, country):
    countryKeyValue = mp.get(catalog['videosByCountry'], country)
    countryList = me.getValue(countryKeyValue)
    

    return countryList


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

def compareLikes(video1, video2):
    """
    Compara la cantidad de likes de dos videos, devuelve verdadero si el primero es mayor que el segundo
    """
    return int(video1['likes']) > int(video2['likes'])


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

def sortVideosByLikes(filteredList, rank):

    sortedList = sa.sort(filteredList, compareLikes)
    sublist = lt.subList(sortedList,1,rank)

    return sublist

# =========================
# Funciones de filtro
# =========================

def filterByTag(list, tag):

    iterator = alit.newIterator(list)
    filteredList = lt.newList('ARRAY_LIST')

    while alit.hasNext(iterator):

        video = alit.next(iterator)
        cleanTag = video['tags'].replace('"','').replace('|','').lower()
        if tag in cleanTag:
            lt.addLast(filteredList, video)
    
    
    return filteredList

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
              str(element['likes']) + "\t" +
              element['dislikes']
              )
        counter += 1

def printReqTwo(oneVideoList):
    video = lt.firstElement(oneVideoList)
    print("title\tchannel_title\tcategory_id\ttrending_time")
    print(video['title'] + "\t" +
          video['channel_title'] + "\t" +
          video['country']+ "\t" +
          str(video['trending_time']))

def printReqThree(oneVideoList):
    video = lt.firstElement(oneVideoList)
    print("title\tchannel_title\tcategory_id\ttrending_time")
    print(video['title'] + "\t" +
          video['channel_title'] + "\t" +
          video['category_id']+ "\t" +
          str(video['trending_time']))

def printReqFour(orderedList):

    iterator = slit.newIterator(orderedList)
    counter = 1
    print("title\tchannel_title\tpublish_time\tviews\tlikes\tdislikes\ttags")

    while slit.hasNext(iterator):

        element = slit.next(iterator)
        print("["+str(counter)+"] " +
              element['title'] + "\t" +
              element['channel_title'] + "\t" +
              element['publish_time'] + "\t" +
              element['views'] + "\t" +
              str(element['likes']) + "\t" +
              element['dislikes']+ "\t" +
              element['tags'] 
              )
        counter += 1
