from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, aliased
from models.user_model import Usuarios_oportuniza, table_usuario
from models.curso_model import Cursos_oportuniza, table_curso

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

table_usuario.metadata.create_all(engine)
table_curso.metadata.create_all(engine)

# Teste a conexão
try:
    connection = engine.connect()
    print("Conexão com o Oracle bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar ao Oracle:", e)
