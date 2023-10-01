from flask_restful import Resource
from models.fbi_usuarios_model import FBIUsuario
import requests
import json
import cx_Oracle

class FBIUsuariosResource(Resource):
    def get(self):
        total_results = 2000
        results_per_page = 20
        total_pages = total_results // results_per_page + 1

        usuarios_fbi = []

        for page_number in range(1, total_pages + 1):

            params = {
                'page': page_number
            }
            response = requests.get(
                'https://api.fbi.gov/wanted/v1/list', params=params)
            data = json.loads(response.content)


            for item in data['items']:
                thumb_url = item['images'][0]['thumb'] if item['images'] else ''
                usuario = FBIUsuario(
                    id=item['uid'],
                    nome=item['title'],
                    descricao=item['description'],
                    sexo=item['sex'],
                    thumbnail=thumb_url,
                    olhos=item['eyes_raw'],
                    idade_maxima=item['age_max'],
                    procurado_agencia='FBI',
                    cabelo=item['hair_raw'],
                    crime=item['poster_classification'],
                    nacionalidade=item['nationality']
                )
                
                usuarios_fbi.append(usuario.__dict__)

        return {'fbi_usuarios': usuarios_fbi}
