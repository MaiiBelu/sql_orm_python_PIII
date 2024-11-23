#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Ing.Jesús Matías González
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Ing.Jesús Matías González"
__email__ = "ingjesusmrgonzalez@gmail.com"
__version__ = "1.1"

import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def fill():
    print('Completemos esta tablita!')

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Se crearán 5 tutores
    Tutor1 = Tutor(name='Martina')
    Tutor2 = Tutor(name='Esteban')
    Tutor3 = Tutor(name='Francisco')
    Tutor4 = Tutor(name='Lina')
    Tutor5 = Tutor(name='Adriana')

    session.add(Tutor1)
    session.add(Tutor2)
    session.add(Tutor3)
    session.add(Tutor4)
    session.add(Tutor5)
    session.commit()
    
     # Se crearán 6 estudiantes
    Estudiante1 = Estudiante(name='Marisa',age=13,grade=1,tutor_id=5)
    Estudiante2 = Estudiante(name='Josefina',age=15,grade=3,tutor_id=1)
    Estudiante3 = Estudiante(name='Eliana',age=15,grade=1,tutor_id=3)
    Estudiante4 = Estudiante(name='Ignacio',age=17,grade=5,tutor_id=1)
    Estudiante5 = Estudiante(name='Antonia',age=14,grade=2,tutor_id=4)
    Estudiante6 = Estudiante(name='Viviana',age=16,grade=4,tutor_id=2)
    
    
    # Agregar estudiantes
    session.add(Estudiante1)
    session.add(Estudiante2)
    session.add(Estudiante3)
    session.add(Estudiante4)
    session.add(Estudiante5)
    session.add(Estudiante6)
    session.commit()


def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante).order_by(Estudiante.id.desc())

    for estudiante in query:
        print(estudiante)


def search_by_tutor(tutor):
    print('Operación búsqueda!')

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)

    for estudiante in query:
        print('Estudiantes de', tutor, estudiante)

def modify(id, name):
    print('Modificando la tabla')

    Session = sessionmaker(bind=engine)
    session = Session()
    
    query = session.query(Tutor).filter(Tutor.name == name )
    idtutor = query.first()
    
    query = session.query(Estudiante).filter(Estudiante.id == id)
    estudiantemod = query.first()
   
    estudiantemod.tutor = idtutor
    
    session.add(estudiantemod)
    session.commit()

    print('Persona actualizada', name)

def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print('Estudiantes en grado:', grade, 'encontradas:', result)

if __name__ == '__main__':
    print("Bienvenidos a otra clase con Python")
    create_schema()   # create and reset database (DB)
    
    fill()
    fetch()

    tutor = 'Martina'
    search_by_tutor(tutor)

    nuevo_tutor = 'Francisco'
    id = 1
    modify(id, nuevo_tutor)

    fetch()

    grade = 2
    count_grade(grade)
