from flask_restful import Resource
from flask import request
from modules.common.gestor_personas import gestor_personas
from modules.apis.auth import jwt_or_login_required

class PersonasResource(Resource):

	@jwt_or_login_required()
	def get(self, persona_id=None):
		if persona_id is None:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
		else:
			resultado=gestor_personas().obtener(persona_id)
			if resultado["Exito"]:
				persona=resultado["Resultado"]
				persona_data=persona.serialize()
				persona_data["birthdate"] = persona.birthdate.strftime('%d-%m-%Y')
				persona_data["pais"]=persona.lugar.pais.nombre
				persona_data["provincia"]=persona.lugar.provincia.nombre
				persona_data["ciudad"]=persona.lugar.ciudad.nombre
				persona_data["barrio"]=persona.lugar.barrio.nombre
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":persona_data}, 200

	@jwt_or_login_required()
	def post(self, recurso=None):
		if (recurso == 'obtener'):
			filtros = request.get_json() 
			personas = gestor_personas().obtener_con_filtro(**filtros)
			personas_data=[]
			for persona in personas:
				pd=persona.serialize()
				pd["birthdate"] = persona.birthdate.strftime('%d-%m-%Y')
				pd["edad"]=persona.age
				pd["genero"]=persona.genero.nombre
				pd["pais"]=persona.lugar.pais.nombre
				pd["provincia"]=persona.lugar.provincia.nombre
				pd["ciudad"]=persona.lugar.ciudad.nombre
				pd["barrio"]=persona.lugar.barrio.nombre
				personas_data.append(pd)
			return {"Exito":True,"MensajePorFallo":"","Resultado":personas_data}, 200
		if (recurso == 'crear'):
			args = request.get_json() 
			resultado=gestor_personas().crear(**args)
			if resultado["Exito"]:
				persona=resultado["Resultado"]
				persona_data=persona.serialize()
				persona_data["birthdate"] = persona.birthdate.strftime('%d-%m-%Y')
				persona_data["pais"]=persona.lugar.pais.nombre
				persona_data["provincia"]=persona.lugar.provincia.nombre
				persona_data["ciudad"]=persona.lugar.ciudad.nombre
				persona_data["barrio"]=persona.lugar.barrio.nombre
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":persona_data}, 201
			else:
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
		
	@jwt_or_login_required()
	def put(self):
		args = request.get_json() 
		resultado = gestor_personas().editar(**args)
		if resultado["Exito"]:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 201
		else:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
		
	@jwt_or_login_required()
	def delete(self, persona_id):
		resultado=gestor_personas().eliminar(persona_id)
		if resultado["Exito"]:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 201
		else:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
