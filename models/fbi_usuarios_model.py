from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base2 = declarative_base()

class FBIUsuario(Base2):
    __tablename__ = 'fbi_usuarios'

    id = Column(String(36), primary_key=True)
    nome = Column(String(255))
    descricao = Column(String(255))
    sexo = Column(String(10))
    thumbnail = Column(String(255))
    olhos = Column(String(20))
    idade_maxima = Column(Integer)
    procurado_agencia = Column(String(50))
    cabelo = Column(String(50))
    crime = Column(String(50))
    nacionalidade = Column(String(50))

    def __init__(self, id, nome, descricao, sexo, thumbnail, olhos, idade_maxima, procurado_agencia, cabelo, crime, nacionalidade):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.sexo = sexo
        self.thumbnail = thumbnail
        self.olhos = olhos
        self.idade_maxima = idade_maxima
        self.procurado_agencia = procurado_agencia
        self.cabelo = cabelo
        self.crime = crime
        self.nacionalidade = nacionalidade
