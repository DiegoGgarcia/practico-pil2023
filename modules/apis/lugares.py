from flask_restful import Resource
from flask import request
from modules.auth import jwt_or_login_required
from modules.common.gestor_lugares import gestor_lugares

class LugaresResource(Resource):
	@jwt_or_login_required()
	def get(self, lugar_type=None):
		if not lugar_type:
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
			return {"Exito":True,"MensajePorFallo":None,"Resultado":lugares_data}, 200
		
		elif (lugar_type=='obtener_paises'):
			paises = gestor_lugares().consultar_paises()
			paises_data = [pais.serialize() for pais in paises]
			return {"Exito":True,"MensajePorFallo":None,"Resultado":paises_data}, 200
		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400

	@jwt_or_login_required()
	def post(self, lugar_type=None):
		if (lugar_type == 'obtener_provincias'):
			data = request.get_json() 
			pais = data.get('pais')
			if not pais:
				return {"Exito":False,"MensajePorFallo":"Debe indicar el pais","Resultado":None}, 400
			provincias = gestor_lugares().consultar_provincias(pais=pais)
			provincias_data = [provincia.serialize() for provincia in provincias]
			return {"Exito":True,"MensajePorFallo":None,"Resultado":provincias_data}, 200
		elif (lugar_type ==  'obtener_ciudades'):
			data = request.get_json() 
			pais = data.get('pais')
			provincia = data.get('provincia')
			if not pais or not provincia:
				return {"Exito":False,"MensajePorFallo":"Debe indicar el pais y provincia","Resultado":None}, 400
			ciudades = gestor_lugares().consultar_ciudades(pais=pais, provincia=provincia)
			ciudades_data = [ciudad.serialize() for ciudad in ciudades]
			return {"Exito":True,"MensajePorFallo":None,"Resultado":ciudades_data}, 200
		elif (lugar_type == 'obtener_barrios'):
			data = request.get_json() 
			pais = data.get('pais')
			provincia = data.get('provincia')
			ciudad = data.get('ciudad')
			if not pais or not provincia or not ciudad:
				return {"Exito":False,"MensajePorFallo":"Debe indicar el pais, provincia y ciudad","Resultado":None}, 400
			barrios = gestor_lugares().consultar_barrios(pais=pais, provincia=provincia, ciudad=ciudad)
			barrios_data = [barrio.serialize() for barrio in barrios]
			return {"Exito":True,"MensajePorFallo":None,"Resultado":barrios_data}, 200
		else:
			return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400

	