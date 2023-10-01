from flask_caching import Cache
import requests
import json
from datetime import datetime, timedelta
from repository.integracaoBD import fetch_fbi_data_from_db

# Inicialize o objeto cache fora da função get_fbi_data
cache = Cache(config={'CACHE_TYPE': 'simple'})

def init_cache(app):
    cache.init_app(app)

def get_fbi_data():
    cached_data = cache.get('fbi_data')
    current_time = datetime.now()

    if cached_data and 'timestamp' in cached_data:
        timestamp = cached_data['timestamp']
        if timestamp.date() == current_time.date():
            data = fetch_fbi_data_from_db()
            print('passei no data')
            return data

    data = fetch_fbi_data()

    data['timestamp'] = current_time
    cache.set('fbi_data', data, timeout=86400)

    return data

def fetch_fbi_data():
    usuarios_fbi = []

    # Iniciar um loop para buscar todas as páginas de resultados
    page_number = 1
    while True:
        params = {
            'page': page_number
        }
        response = requests.get(
            'https://api.fbi.gov/wanted/v1/list', params=params)
        data = json.loads(response.content)
        
        # Verificar se há resultados nesta página
        if not data['items']:
            break
        
        for item in data['items']:
            thumb_url = item['images'][0]['thumb'] if item['images'] else ''
            usuario = {
                'id': item['uid'],
                'nome': item['title'],
                'descricao': item['description'],
                'sexo': item['sex'],
                'thumbnail': thumb_url,
                'olhos': item['eyes_raw'],
                'idade_maxima': item['age_max'],
                'procurado_agencia': 'FBI',
                'cabelo': item['hair_raw'],
                'crime': item['poster_classification'],
                'nacionalidade': item['nationality']
            }
            usuarios_fbi.append(usuario)
        
        page_number += 1

    return {'fbi_usuarios': usuarios_fbi}
