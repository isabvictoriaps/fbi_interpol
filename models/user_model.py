from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

table_usuario = declarative_base()

class Usuarios_oportuniza(table_usuario):
    __tablename__ = 'user_oportuniza'

    id = Column(String(255), primary_key=True)
    nome_completo = Column(String(255))
    usuario = Column(String(255))
    email = Column(String(255))
    senha = Column(String(255))
    img_usuario = Column(String(255))
    

    def __init__(self, id, nome_completo, usuario, email, senha, img_usuario):
        self.id = id
        self.nome_completo = nome_completo
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.img_usuario = img_usuario

  