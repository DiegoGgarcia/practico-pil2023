from flask_restful import Resource
from modules.auth import jwt_or_login_required
from modules.common.gestor_generos import gestor_generos

class GenerosResource(Resource):
	@jwt_or_login_required()
	def get(self):
		generos = gestor_generos().obtener_todo()
		generos_data = [genero.serialize() for genero in generos]
		return {"Exito":True,"MensajePorFallo":None,"Resultado":generos_data}, 200
