from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, aliased
from models.fbi_usuarios_model import FBIUsuario
from models.interpol_usuarios_model import InterpolUsuario, Base
from models.fbi_usuarios_model import FBIUsuario, Base2

# Configurar a URL de conexão
username = 'RM96104'
password = '120903'
host = 'oracle.fiap.com.br'
port = '1521'
sid = 'ORCL'  # Ou use o serviço

# Crie a URL de conexão
connection_url = f'oracle+cx_oracle://{username}:{password}@{host}:{port}/{sid}'

# Crie a engine de conexão
engine = create_engine(connection_url)

# criando sessão com o Banco de Dados
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
Base2.metadata.create_all(engine)


def fetch_fbi_user_by_id(user_id):
    # Consultar o banco de dados para encontrar um usuário pelo ID
    user = session.query(FBIUsuario).filter_by(id=user_id).first()
    return user


def fetch_fbi_data_from_db():
    usuarios_fbi = session.query(FBIUsuario).all()

    # Crie uma lista de dicionários a partir dos objetos SQLAlchemy
    data = [
        {
            'id': result.id,
            'nome': result.nome,
            'descricao': result.descricao,
            'sexo': result.sexo,
            'thumbnail': result.thumbnail,
            'olhos': result.olhos,
            'idade_maxima': result.idade_maxima,
            'procurado_agencia': result.procurado_agencia,
            'cabelo' :result.cabelo,
            'crime': result.crime,
            'nacionalidade':result.nacionalidade,
        }
        for result in usuarios_fbi
    ]
    return {'fbi_usuarios': data}

def fetch_interpol_user_by_id(user_id):
    # Consultar o banco de dados para encontrar um usuário pelo ID
    user = session.query(InterpolUsuario).filter_by(id=user_id).first()
    return user


def fetch_interpol_data_from_db():
    usuarios_interpol = session.query(InterpolUsuario).all()

    # Crie uma lista de dicionários a partir dos objetos SQLAlchemy
    data = [
        {
            'id': result.id,
            'nome': result.nome,
            'descricao': result.descricao,
            'sexo': result.sexo,
            'thumbnail': result.thumbnail,
            'olhos': result.olhos,
            'nascimento': result.nascimento,
            'procurado_agencia': result.procurado_agencia,
            'cabelo': result.cabelo,
            'crime': result.crime,
            'nacionalidade': result.nacionalidade,
        }
        for result in usuarios_interpol
    ]

    # Agora você pode serializar a lista de dicionários em JSON
    return {'interpol_usuarios': data}

# Teste a conexão
try:
    connection = engine.connect()
    print("Conexão com o Oracle bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar ao Oracle:", e)


