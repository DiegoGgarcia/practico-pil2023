from flask_restful import Resource
from flask import request
from modules.auth import jwt_or_login_required
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_personas import gestor_personas
from modules.common.gestor_carreras import gestor_carreras

class CarrerasResource(Resource):
	@jwt_or_login_required()
	def get(self, recurso=None):
		if not recurso:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
		
		elif recurso == "obtener_universidades":
			universidades = gestor_carreras().obtener_universidades()

			universidades_data=[]
			for cadaUna in universidades:
				pd=cadaUna.serialize()
				universidades_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":universidades_data}, 200

		elif recurso == "obtener_roles":
			roles = gestor_carreras().obtener_roles()

			roles_data=[]
			for cadaUna in roles:
				pd=cadaUna.serialize()
				roles_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":roles_data}, 200

		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
	
	@jwt_or_login_required()
	def post(self, recurso=None):
		if not recurso:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
		
		elif recurso == "obtener_carreras":
			data = request.get_json() 
			persona_id = data.get('id_persona')
			if not persona_id:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una persona","Resultado":None}, 400
			
			persona = gestor_personas().obtener(persona_id)
			if not persona["Exito"]:
				return {"Exito":False,"MensajePorFallo":persona["MensajePorFallo"],"Resultado":None}, 400
			
			carreras=gestor_carreras_personas().obtener_carreras_por_persona(persona["Resultado"])

			carreras_data=[]
			for cadaUna in carreras:
				pd=cadaUna.serialize()
				pd["universidad"]=cadaUna.carrera.universidad.nombre
				pd["facultad"]=cadaUna.carrera.facultad.nombre
				pd["campus"]=cadaUna.carrera.campus.nombre
				pd["programa"]=cadaUna.carrera.programa.nombre
				pd["rol"]=cadaUna.tipopersona.nombre
				carreras_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":carreras_data}, 200

		elif recurso == "obtener_facultades":
			data = request.get_json() 
			universidad = data.get('universidad')
			if not universidad:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una Universidad","Resultado":None}, 400

			facultades = gestor_carreras().obtener_facultades(universidad=universidad)

			facultades_data=[]
			for cadaUna in facultades:
				pd=cadaUna.serialize()
				facultades_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":facultades_data}, 200

		elif recurso == "obtener_campus":
			data = request.get_json() 
			universidad = data.get('universidad')
			facultad = data.get('facultad')
			if not universidad or not facultad:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una Universidad / Facultad","Resultado":None}, 400

			campus = gestor_carreras().obtener_campus(universidad=universidad, facultad=facultad)

			campus_data=[]
			for cadaUna in campus:
				pd=cadaUna.serialize()
				campus_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":campus_data}, 200
		
		elif recurso == "obtener_programas":
			data = request.get_json() 
			universidad = data.get('universidad')
			facultad = data.get('facultad')
			campus = data.get('campus')
			if not universidad or not facultad or not campus:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una Universidad / Facultad / Campus","Resultado":None}, 400

			programas = gestor_carreras().obtener_programas(universidad=universidad, facultad=facultad, campus=campus)

			programas_data=[]
			for cadaUna in programas:
				pd=cadaUna.serialize()
				programas_data.append(pd)
			return {"Exito":True,"MensajePorFallo":None,"Resultado":programas_data}, 200

		elif recurso == "asignar_carrera":
			data = request.get_json() 
			universidad = data.get('universidad')
			facultad = data.get('facultad')
			campus = data.get('campus')
			programa = data.get('programa')
			rol = data.get('rol')
			id_persona = data.get('id_persona')
			if not universidad or not facultad or not campus or not programa or not rol:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una Universidad / Facultad / Campus / Programa / Rol","Resultado":None}, 400

			programas = gestor_carreras_personas().asignar_carrera(universidad=universidad, facultad=facultad, campus=campus, programa=programa,rol=rol, id_persona=id_persona)

			return {"Exito":True,"MensajePorFallo":None,"Resultado":None}, 200
						
		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400



	@jwt_or_login_required()
	def delete(self, recurso=None):
		if not recurso:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
		
		elif recurso == "eliminar":
			data = request.get_json() 
			carrera_persona_id = data.get('id')
			if not carrera_persona_id:
				return {"Exito":False,"MensajePorFallo":"Debe indicar una carrera","Resultado":None}, 400
			
			resultado=gestor_carreras_personas().eliminar(carrera_persona_id)
			if resultado["Exito"]:
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 201
			else:
				return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400


		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400
