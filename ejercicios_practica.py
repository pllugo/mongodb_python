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

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import json

import tinymongo as tm
import tinydb

# Bug: https://github.com/schapman1974/tinymongo/issues/58
class TinyMongoClient(tm.TinyMongoClient):
    @property
    def _storage(self):
        return tinydb.storages.JSONStorage

db_name = 'secundaria'


def clear():
    conn = TinyMongoClient()
    db = conn[db_name]

    # Eliminar todos los documentos que existan en la coleccion estudiante
    db.estudiante.remove({})

    # Cerrar la conexión con la base de datos
    conn.close()

def insert_persona(name, age, grade, tutor):
    conn = TinyMongoClient()
    db = conn[db_name]

    # Insertar un documento
    persona_json = {"name": name, "age": age, "grade": grade, "tutor": tutor}
    db.estudiante.insert_one(persona_json)


    # Cerrar la conexión con la base de datos
    conn.close()

def fill():
    print('Completemos esta tablita!')
    # Llenar la coleccion "estudiante" con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto completado por mongo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> nombre de su tutor

    # Se debe utilizar la sentencia insert_one o insert_many.
    insert_persona('Pedro', 36, 6, 'Patricia')
    insert_persona('Carolina', 29, 3, 'Juan')
    insert_persona('Alejandro', 21, 2, 'Roberto')
    insert_persona('Maria', 19, 1, 'Adolfo')
    insert_persona('Bryant', 26, 3, 'Magy')


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
        cursor = db.estudiante.find()
        data = list(cursor)
        json_string = json.dumps(data, indent=4)
        print(json_string)
    else:
        # Leer todos los documentos y obtener los datos de a uno
        cursor = db.estudiante.find()
        for doc in cursor:
            print(doc)

    # Cerrar la conexión con la base de datos
    conn.close()


def find_by_grade(grade):
    print('Operación búsqueda!')
    # Utilizar la sentencia find para imprimir en pantalla
    # aquellos estudiantes que se encuentra en en año "grade"

    # De la lista de esos estudiantes debe imprimir
    # en pantalla unicamente los siguiente campos por cada uno:
    # id / name / age

    # Conectarse a la base de datos
    conn = TinyMongoClient()
    db = conn[db_name]

    # Encontrar los estudiantes que tengan el mismo grado
    personas = db.estudiante.find({"grade": grade})
    for data in personas:
        print('Los estudiantes son: name = {}, age = {}, id = {}'.format(data['name'], data['age'], data['_id']))
    # Cerrar la conexión con la base de datos
    conn.close()


def insert(student):
    print('Nuevos ingresos!')
    # Utilizar la sentencia insert_one para ingresar nuevos estudiantes
    # a la secundaria

    # El parámetro student deberá ser un JSON el cual se inserta en la db
    # Conectarse a la base de datos
    conn = TinyMongoClient()
    db = conn[db_name]
    db.estudiante.insert_one(student)
    # Cerrar la conexión con la base de datos
    conn.close()


def count(grade):
    print('Contar estudiantes')
    # Utilizar la sentencia find + count para contar
    # cuantos estudiantes pertenecen el grado "grade"
    conn = TinyMongoClient()
    db = conn[db_name]
    resultado = db.estudiante.find({"grade": grade}).count()
    print('Los estudiantes son:', resultado)
    # Cerrar la conexión con la base de datos
    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    # Borrar la db
    clear()
    
    fill()
    show()

    grade = 3
    find_by_grade(grade)

    student = {
                    "name": "Luis",
                    "age": 37,
                    "grade": 5,
                    "tutor": "Juana"
                }
    insert(student)
    show()

    count(grade)
