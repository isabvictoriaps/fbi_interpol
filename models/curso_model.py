from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

table_curso = declarative_base()

class Cursos_oportuniza(table_curso):
    __tablename__ = 'curso_oportuniza'

    id_curso = Column(String(255), primary_key=True)
    nome_curso = Column(String(255))
    empresa_curso = Column(String(255))
    img_curso = Column(String(1000))
    link_curso = Column(String(1000))
    

    def __init__(self, id_curso, nome_curso, empresa_curso, img_curso, link_curso):
        self.id_curso = id_curso
        self.nome_curso = nome_curso
        self.empresa_curso = empresa_curso
        self.img_curso = img_curso
        self.link_curso = link_curso

  