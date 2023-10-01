from flask_caching import Cache
import requests
from flask import jsonify
from datetime import datetime, timedelta
from repository.integracaoBD import fetch_interpol_user_by_id, fetch_interpol_data_from_db, session
from models.interpol_usuarios_model import InterpolUsuario

cache = Cache(config={'CACHE_TYPE': 'simple'})

def init_cache2(app):
    cache.init_app(app)

def get_all_interpol_data():
    cached_data = cache.get('interpol_data')
    current_time = datetime.now()

    if cached_data and 'timestamp' in cached_data:
        timestamp = cached_data['timestamp']
        if timestamp.date() == current_time.date():
            data = cached_data
            print('Pegando dados do cache')
            return data

    all_data = fetch_all_interpol_data()
    
    all_data['timestamp'] = current_time
    cache.set('interpol_data', all_data, timeout=86400)

    return all_data

# ... (código anterior) ...

def fetch_all_interpol_data():
    results_per_page = 160
    usuarios_interpol = []

    # Iniciar um loop para buscar todas as páginas de resultados
    page_number = 1
    while True:
        params = {
            'page': page_number,
            'resultPerPage': results_per_page
        }

        response = requests.get('https://ws-public.interpol.int/notices/v1/red', params=params)
        if response.status_code == 200:
            print(f"Requisição bem-sucedida para a página {page_number}")
            data = response.json()
            print(data)
            
            # Verifique se '_embedded' e 'notices' existem no objeto data
            if '_embedded' in data and 'notices' in data['_embedded']:
                for item in data['_embedded']['notices']:
                    usuario_id = item['entity_id'].replace('/', '%2F')
                    response2 = requests.get(f'https://ws-public.interpol.int/notices/v1/red/{usuario_id}')
                            
                    if response2.status_code == 200:
                        print('Status code 200')
                        data2 = response2.json()
                        
                        # Verifique se o usuário já existe no banco de dados
                        usuario_existente = fetch_interpol_user_by_id(data2['entity_id'])

                        if usuario_existente:
                            # Atualize os campos do usuário existente com os novos valores
                            if data2.get('forename') and data2.get('name'):
                                usuario_existente.nome = data2['forename'] + ' ' + data2['name']
                            if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants']:
                                usuario_existente.descricao = data2['arrest_warrants']['charge']
                            if 'sex_id' in data2:
                                usuario_existente.sexo = data2['sex_id'][0]
                            if '_links' in data2 and 'thumbnail' in data2['_links']:
                                usuario_existente.thumbnail = data2['_links']['thumbnail']['href']
                            if data2.get('eyes_colors_id'):
                                usuario_existente.olhos = ', '.join(data2['eyes_colors_id'])
                            if 'date_of_birth' in data2:
                                usuario_existente.nascimento = data2['date_of_birth']
                            usuario_existente.procurado_agencia = 'Interpol'
                            if data2.get('hairs_id'):
                                usuario_existente.cabelo = ', '.join(data2['hairs_id'])
                            if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants']:
                                usuario_existente.crime = data2['arrest_warrants']['charge']
                            if data2.get('nationalities'):
                                usuario_existente.nacionalidade = ', '.join(data2['nationalities'])
                            usuarios_interpol.append({
                                'id': usuario_existente.id,
                                'nome': usuario_existente.nome,
                                'descricao': usuario_existente.descricao,
                                'sexo': usuario_existente.sexo,
                                'thumbnail': usuario_existente.thumbnail,
                                'olhos': usuario_existente.olhos,
                                'nascimento': usuario_existente.nascimento,
                                'procurado_agencia': usuario_existente.procurado_agencia,
                                'cabelo': usuario_existente.cabelo,
                                'crime': usuario_existente.crime,
                                'nacionalidade': usuario_existente.nacionalidade
                            })
                            print(usuarios_interpol)
                        else:
                            # Crie um novo registro se o usuário não existir
                            nome = data2['forename'] + ' ' + data2['name'] if data2.get('forename') and data2.get('name') else ''
                            descricao = data2['arrest_warrants']['charge'] if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants'] else ''
                            sexo = data2['sex_id'][0] if 'sex_id' in data2 else ''
                            thumbnail = data2['_links']['thumbnail']['href'] if '_links' in data2 and 'thumbnail' in data2['_links'] else ''
                            olhos = ', '.join(data2['eyes_colors_id']) if data2.get('eyes_colors_id') else ''
                            nascimento = data2['date_of_birth'] if 'date_of_birth' in data2 else ''
                            cabelo = ', '.join(data2['hairs_id']) if data2.get('hairs_id') else ''
                            crime = data2['arrest_warrants']['charge'] if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants'] else ''
                            nacionalidade = ', '.join(data2['nationalities']) if data2.get('nationalities') else ''

                            usuario = InterpolUsuario(
                                id=data2['entity_id'],
                                nome=nome,
                                descricao=descricao,
                                sexo=sexo,
                                thumbnail=thumbnail,
                                olhos=olhos,
                                nascimento=nascimento,
                                procurado_agencia='Interpol',
                                cabelo=cabelo,
                                crime=crime,
                                nacionalidade=nacionalidade
                            )
                            session.add(usuario)
                            usuarios_interpol.append({
                                'id': usuario.id,
                                'nome': usuario.nome,
                                'descricao': usuario.descricao,
                                'sexo': usuario.sexo,
                                'thumbnail': usuario.thumbnail,
                                'olhos': usuario.olhos,
                                'nascimento': usuario.nascimento,
                                'procurado_agencia': usuario.procurado_agencia,
                                'cabelo': usuario.cabelo,
                                'crime': usuario.crime,
                                'nacionalidade': usuario.nacionalidade
                            })
                            print('Usuário adicionado ao banco de dados', usuario)
                    
                session.commit()
            print('USUARIOSSSSSSSS',usuarios_interpol)
            # Verifique se há mais páginas para buscar
            if '_links' in data and 'next' in data['_links']:
                page_number += 1
                print('ENTROU NO IF')
            else:
                return {'usuarios_interpol': usuarios_interpol}
