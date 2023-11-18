from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from service.user_service import fetch_user_by_username, fetch_user_by_email, add_user_to_db
from uuid import uuid4

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from service.user_service import fetch_user_by_username, fetch_user_by_email, add_user_to_db
from uuid import uuid4

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from service.user_service import fetch_user_by_username, fetch_user_by_email, add_user_to_db
from uuid import uuid4

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/cadastro_usuario', methods=['POST'])
def cadastro_usuario():
    if request.method == 'POST':
        data = request.get_json()

        required_fields = ['nome_completo', 'usuario', 'email', 'confirm_email', 'senha', 'confirm_senha']

        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'O campo {field} não pode ser nulo'}), 400

        nome_completo, usuario, email, confirm_email, senha, confirm_senha = (
            data.get(key) for key in required_fields
        )

        hashed_password = pbkdf2_sha256.hash(senha)

        if email != confirm_email:
            return jsonify({'message': 'E-mails não coincidem'}), 400

        if senha != confirm_senha:
            return jsonify({'message': 'Senhas não coincidem'}), 400

        existing_user_by_username = fetch_user_by_username(usuario)
        if existing_user_by_username:
            return jsonify({'message': 'Nome de usuário já existe'}), 400

        existing_user_by_email = fetch_user_by_email(email)
        if existing_user_by_email:
            return jsonify({'message': 'E-mail já cadastrado'}), 400

        add_user_to_db(id=str(uuid4()), nome_completo=nome_completo, usuario=usuario, email=email, senha=hashed_password)
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        username_or_email = data.get('username_or_email')
        password = data.get('password')

        print(username_or_email)
        print(password)

        # Buscar o usuário pelo nome de usuário ou email
        user = fetch_user_by_username(username_or_email) or fetch_user_by_email(username_or_email)
        print(user)

        if user and pbkdf2_sha256.verify(password, user.senha):
            print('login bem-vindo')
            return jsonify({'message': 'Login bem-sucedido'}), 200
        else:
            return jsonify({'message': 'Credenciais inválidas'}), 401