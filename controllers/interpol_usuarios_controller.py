from flask_restful import Resource
from models.interpol_usuarios_model import InterpolUsuario
import requests
import json

class InterpolUsuariosResource(Resource):
    def get(self):
        total_results = 2000
        results_per_page = 20
        total_pages = (total_results + results_per_page - 1) // results_per_page  # Arredonda para cima

        usuarios_interpol = []

        for page_number in range(1, total_pages + 1):
            params = {
                'page': page_number,
                'resultPerPage': results_per_page
            }

            response = requests.get('https://ws-public.interpol.int/notices/v1/red', params=params)

            if response.status_code == 200:
                try:
                    data = response.json()
                    # Faça o que você precisa com os dados da primeira requisição
                    for item in data['_embedded']['notices']:
                        usuario_id = item['entity_id'].replace('/', '%2F')
                        response2 = requests.get(f'https://ws-public.interpol.int/notices/v1/red/{usuario_id}')
                        
                        if response2.status_code == 200:
                            try:
                                data2 = response2.json()
                                
                                # Crie o objeto InterpolUsuario com os dados de data2
                                usuario = InterpolUsuario(
                                    id=data2['entity_id'],
                                    nome=data2['forename'] + ' ' + data2['name'],
                                    descricao=data2['arrest_warrants']['charge'] if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants'] else '',
                                    sexo=data2['sex_id'][0] if 'sex_id' in data2 else '',
                                    thumbnail=data2['_links']['thumbnail']['href'] if '_links' in data2 and 'thumbnail' in data2['_links'] else '',
                                    olhos=data2['eyes_colors_id'],
                                    nascimento=data2['date_of_birth'],
                                    procurado_agencia='Interpol',
                                    cabelo = data2['hairs_id'],
                                    crime=data2['arrest_warrants']['charge'] if 'arrest_warrants' in data2 and 'charge' in data2['arrest_warrants'] else '',
                                    nacionalidade=data2['nationalities']
                                )
                                usuarios_interpol.append(usuario.__dict__)
                            except json.decoder.JSONDecodeError:
                                data2 = {'error': 'A resposta da segunda requisição não é um JSON válido'}
                        else:
                            data2 = {'error': f'Erro na segunda requisição: {response2.status_code}'}
                        
                except json.decoder.JSONDecodeError:
                    data = {'error': 'A resposta da primeira requisição não é um JSON válido'}
            else:
                data = {'error': f'Erro na primeira requisição: {response.status_code}'}
        
        return {'usuarios_interpol': usuarios_interpol}
