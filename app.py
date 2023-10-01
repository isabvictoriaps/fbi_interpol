from flask import Flask
from flask_restful import Api
from controllers.fbi_usuarios_controller import FBIUsuariosResource  
from controllers.interpol_usuarios_controller import InterpolUsuariosResource

app = Flask(__name__)
api = Api(app)

api.add_resource(FBIUsuariosResource, '/fbiusuarios')
api.add_resource(InterpolUsuariosResource, '/interpolusuarios')

if __name__ == '__main__':
    app.run(debug=True)
