from models.curso_model import Cursos_oportuniza 
from repository.integracaoBD import session, Session
import cloudinary
from config import cloudinary

def add_curso_to_db(id_curso, nome_curso, empresa_curso, img_curso, link_curso):
    try:
        novo_curso = Cursos_oportuniza(id_curso=id_curso, nome_curso=nome_curso, empresa_curso=empresa_curso, img_curso=img_curso, link_curso=link_curso)
        session.add(novo_curso)
        session.commit()
        print("Curso adicionado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar curso: {e}")
    finally:
        session.close()


# Função para buscar curso pelo id
def fetch_curso_by_id(id_curso):
    session = Session()
    curso = session.query(Cursos_oportuniza).filter_by(id_curso=id_curso).first()
    session.close()
    return curso

# Função para buscar curso pelo nome da empresa
def fetch_curso_by_empresa(nome_empresa):
    session = Session()
    curso = session.query(Cursos_oportuniza).filter_by(nome_empresa=nome_empresa).first()
    session.close()
    return curso

def upload_imagem_curso(imagem_base64):
    response = cloudinary.uploader.upload(imagem_base64)
    return response['secure_url']