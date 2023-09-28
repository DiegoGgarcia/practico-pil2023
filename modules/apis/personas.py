from flask_restful import Resource
from flask import request
from modules.common.gestor_personas import gestor_personas
from modules.auth import jwt_or_login_required

class PersonasResource(Resource):

	@jwt_or_login_required()
	def get(self, persona_id=None):
		if persona_id is None:
			data = request.get_json() 
			pagina = data.get('pagina') 
			filtros = data.get('filtros', {})
			personas, total_paginas = gestor_personas().obtener_pagina(pagina, **filtros)
			personas_data=[]
			for persona in personas:
				pd=persona.serialize()
				pd["birthdate"]=persona.birthdate.isoformat()
				pd["genero"]=persona.genero.nombre
				pd["pais"]=persona.lugar.pais.nombre
				pd["provincia"]=persona.lugar.provincia.nombre
				pd["ciudad"]=persona.lugar.ciudad.nombre
				pd["barrio"]=persona.lugar.barrio.nombre
				personas_data.append(pd)
			return {"Exito":True,"MensajePorFallo":"","Resultado":personas_data,"TotalPaginas":total_paginas}, 200
		else:
			resultado=gestor_personas().obtener(persona_id)
			if resultado["Exito"]:
				persona=resultado["Resultado"]
				persona_data=persona.serialize()
				persona_data["birthdate"]=persona.birthdate.isoformat()
				persona_data["pais"]=persona.lugar.pais.nombre
				persona_data["provincia"]=persona.lugar.provincia.nombre
				persona_data["ciudad"]=persona.lugar.ciudad.nombre
				persona_data["barrio"]=persona.lugar.barrio.nombre
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":persona_data}, 200
			else:
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400

	@jwt_or_login_required()
	def post(self):
		args = request.get_json() 
		resultado=gestor_personas().crear(**args)
		if resultado["Exito"]:
			persona=resultado["Resultado"]
			persona_data=persona.serialize()
			persona_data["birthdate"]=persona.birthdate.isoformat()
			persona_data["pais"]=persona.lugar.pais.nombre
			persona_data["provincia"]=persona.lugar.provincia.nombre
			persona_data["ciudad"]=persona.lugar.ciudad.nombre
			persona_data["barrio"]=persona.lugar.barrio.nombre
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":persona_data}, 201
		else:
			return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
		
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
