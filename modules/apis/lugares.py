from flask_restful import Resource, reqparse
from flask import jsonify, request
from flask_login import login_required
from modules.common.gestor_lugares import gestor_lugares
from flask_jwt_extended import jwt_required, get_jwt_identity

class LugaresResource(Resource):
	@jwt_required()
	def get(self):
		data = request.get_json() 

		pais = data.get('pais')
		provincia = data.get('provincia')
		ciudad = data.get('ciudad')
		barrio = data.get('barrio')

		lugares = gestor_lugares().consultar_lugares(
			pais=pais,
			provincia=provincia,
			ciudad=ciudad,
			barrio=barrio)

		lugares_data=[]
		for lugar in lugares:
			pd=lugar.serialize()
			pd["pais"]=lugar.pais.nombre
			pd["provincia"]=lugar.provincia.nombre
			pd["ciudad"]=lugar.ciudad.nombre
			pd["barrio"]=lugar.barrio.nombre
			lugares_data.append(pd)
		return jsonify(lugares_data)