from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class InterpolUsuario(Base):
    __tablename__ = 'interpol_usuarios'

    id = Column(String(50), primary_key=True)
    nome = Column(String(300))
    descricao = Column(String(700))
    sexo = Column(String(10))
    thumbnail = Column(String(400))
    olhos = Column(String(50))
    nascimento = Column(String(50))
    procurado_agencia = Column(String(50))
    cabelo = Column(String(50))
    crime = Column(String(50))
    nacionalidade = Column(String(50))

    def __init__(self, id, nome, descricao, sexo, thumbnail, olhos, nascimento, procurado_agencia, cabelo, crime, nacionalidade):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.sexo = sexo
        self.thumbnail = thumbnail
        self.olhos = olhos
        self.nascimento = nascimento
        self.procurado_agencia = procurado_agencia
        self.cabelo = cabelo
        self.crime = crime
        self.nacionalidade = nacionalidade
