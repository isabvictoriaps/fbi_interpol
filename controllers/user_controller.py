from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from service.curso_service import fetch_curso_by_id, fetch_curso_by_empresa, add_curso_to_db, upload_imagem_curso, buscar_cursos, curso_to_dict
from service.user_service import fetch_user_by_username, fetch_user_by_email, add_user_to_db, upload_imagem_usuario
from uuid import uuid4

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/cadastro_usuario', methods=['POST'])
def cadastro_usuario():
    if request.method == 'POST':
        data = request.form
        img_usuario = request.files.get('img_usuario')  # Use get para evitar KeyError

        required_fields = ['nome_completo', 'usuario', 'email', 'confirm_email', 'senha', 'confirm_senha']

        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'O campo {field} não pode ser nulo'}), 400

        nome_completo, usuario, email, confirm_email, senha, confirm_senha = (
            data.get(key) for key in required_fields
        )

        if not img_usuario:
            return jsonify({'message': 'O campo img_usuario não pode ser nulo'}), 400

        img_usuario = upload_imagem_curso(img_usuario)  # Chama a função para upload da imagem

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

        add_user_to_db(id=str(uuid4()), nome_completo=nome_completo, usuario=usuario, email=email, senha=hashed_password, img_usuario=img_usuario)
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201

@app.route('/usuario/<string:usuario>', methods=['GET'])
def obter_usuario(usuario):
    user = fetch_user_by_username(usuario)

    if user:
        return jsonify({
            'id': user.id,
            'nome_completo': user.nome_completo,
            'usuario': user.usuario,
            'email': user.email,
            'img_usuario': user.img_usuario
        })
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404
        
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
            usuario_retorno = user.usuario if user.usuario else user.email
            return jsonify({'message': 'Login bem-sucedido', 'usuario': usuario_retorno}), 200
        else:
            return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/curso', methods=['POST'])
def cadastro_curso():
    if request.method == 'POST':
        data = request.form
        arquivo = request.files['img_curso']  # Use request.files para dados de formulário multipartes

        id_curso = str(uuid4())
        nome_curso = data.get('nome_curso')
        empresa_curso = data.get('empresa_curso')
        img_curso = upload_imagem_curso(arquivo)  # Chama a função para upload da imagem
        link_curso = data.get('link_curso')

        add_curso_to_db(id_curso, nome_curso, empresa_curso, img_curso, link_curso)

    return jsonify({'message': 'Curso cadastrado com sucesso'}), 201

@app.route('/curso', methods=['GET'])
def busca_curso():
    cursos = buscar_cursos()
    cursos_dicts = [curso_to_dict(curso) for curso in cursos]
    return jsonify(cursos_dicts)
