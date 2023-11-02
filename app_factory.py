import os
from flask import Flask
from flask_restful import Api
from modules.apis.personas import PersonasResource
from modules.apis.lugares import LugaresResource
from modules.apis.generos import GenerosResource
from modules.apis.carreras import CarrerasResource
from modules.apis.auth import AuthResource
from modules.models.base import db 
from config import db_connector, db_user, db_password, db_ip_address, db_name
from flask_jwt_extended import JWTManager
from modules.models.entities import User

def create_app():
	app = Flask(__name__)
	app.secret_key = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"

	db.init_app(app)
	api=Api(app)
	jwt = JWTManager(app)

	with app.app_context():
		db.create_all()
		usuario=User(username=os.getenv("DEFAULT_USER"), password=os.getenv("DEFAULT_PASSWORD"))
		usuario.guardar()

	api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>', '/api/personas/<string:recurso>')
	api.add_resource(LugaresResource, '/api/lugares', '/api/lugares/<string:lugar_type>')
	api.add_resource(CarrerasResource, '/api/carreras', '/api/carreras/<string:recurso>')
	api.add_resource(GenerosResource, '/api/generos')
	api.add_resource(AuthResource, '/api/login')

	return app
