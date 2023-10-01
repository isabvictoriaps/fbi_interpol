from flask import Flask, jsonify
from services.interpol_service import init_cache2, get_all_interpol_data
from services.fbi_service import init_cache, get_fbi_data
from flask_restful import Api
from datetime import datetime, timedelta

app = Flask(__name__)
init_cache(app)
init_cache2(app)

@app.route('/fbi_data', methods=['GET'])
def fbi_data():
    try:
        data = get_fbi_data()
        # Certifique-se de que 'data' é um dicionário serializável em JSON
        return jsonify({'fbi_data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/interpol_data', methods=['GET'])
def interpol_data():
    global last_interpol_data_fetch

    try:
        data = get_all_interpol_data()
        # Certifique-se de que 'data' é um dicionário serializável em JSON
        return jsonify({'fbi_data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
