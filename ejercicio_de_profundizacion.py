#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Pedro Luis Lugo Garcia"
__email__ = "pllugo@gmail.com"
__version__ = "1.1"

import json
import requests
import tinymongo as tm
import tinydb

# Bug: https://github.com/schapman1974/tinymongo/issues/58
class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

db_name = 'tarea'

def clear():
    conn = TinyMongoClient()
    db = conn[db_name]

    # Eliminar todos los documentos que existan en la coleccion estudiante
    db.datos.remove({})

    # Cerrar la conexión con la base de datos
    conn.close()

def fill():
    print('Ingresemos los datos de la url')
    conn = TinyMongoClient()
    db = conn[db_name]

    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data = response.json()

    db.datos.insert_many(data)
    # Cerrar la conexión con la base de datos
    conn.close()

def show(fetch_all=True):
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia find para imprimir en pantalla
    # todos los documentos de la DB
    # Queda a su criterio serializar o no el JSON "dumps"
    #  para imprimirlo en un formato más "agradable"
    # Conectarse a la base de datos
    conn = TinyMongoClient()
    db = conn[db_name]

    # Leer todos los documentos y obtener todos los datos juntos
    if fetch_all is True:
        cursor = db.datos.find()
        data = list(cursor)
        json_string = json.dumps(data, indent=4)
        print(json_string)
    else:
        # Leer todos los documentos y obtener los datos de a uno
        cursor = db.datos.find()
        for doc in cursor:
            print(doc)

    # Cerrar la conexión con la base de datos
    conn.close()

def title_completed_count(userId):
    conn = TinyMongoClient()
    db = conn[db_name]
    resultado = db.datos.find({"userId": userId, "completed": True}).count()
    print('El userId: {} tiene {} titulos completos'.format(userId, resultado))
    #contador = 0
    #for data in resultado:
     #   if data['completed'] == True:
      #      contador += 1
       # else:
        #    continue
    #print(contador)
    # Cerrar la conexión con la base de datos
    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    # Borrar la DB
    clear()

    # Completar la DB con el JSON request
    fill()
    #show()

    # Buscar autor
    userId = 5
    title_completed_count(userId)