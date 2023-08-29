from modules.common.gestor_comun import ResponseMessage
from modules.models.entities import Pais, Provincia, Ciudad, Barrio, Lugar, db

class gestor_lugares(ResponseMessage):
	def __init__(self):
		super().__init__()
	
	def consultar_lugares(self, **kwargs):

		query = db.session.query(Lugar)

		if 'pais' in kwargs and kwargs["pais"]:
			query = query.join(Pais).filter(Pais.nombre == kwargs["pais"])
		if 'provincia' in kwargs and kwargs["provincia"]:
			query = query.join(Provincia).filter(Provincia.nombre == kwargs["provincia"])
		if 'ciudad' in kwargs and kwargs["ciudad"]:
			query = query.join(Ciudad).filter(Ciudad.nombre == kwargs["ciudad"])
		if 'barrio' in kwargs and kwargs["barrio"]:
			query = query.join(Barrio).filter(Barrio.nombre == kwargs["barrio"])

		lugares = query.all()

		return lugares
	
	def consultar_paises(self, **kwargs):
		paises = db.session.query(Pais).distinct().join(Lugar).all()
		return paises
	
	def consultar_provincias(self, **kwargs):
		provincias = (
			db.session.query(Provincia)
			.distinct()
			.join(Lugar)
			.join(Pais)
			.filter(Pais.nombre == kwargs["pais"])
			.all()
		)
		return provincias

	def consultar_ciudades(self, **kwargs):
		ciudades = (
			db.session.query(Ciudad)
			.distinct()
			.join(Lugar)
			.join(Pais)
			.join(Provincia)
			.filter(Pais.nombre == kwargs["pais"], Provincia.nombre == kwargs["provincia"])
			.all()
		)
		return ciudades

	def consultar_barrios(self, **kwargs):
		barrios = (
			db.session.query(Barrio)
			.distinct()
			.join(Lugar)
			.join(Pais)
			.join(Provincia)
			.join(Ciudad)
			.filter(Pais.nombre == kwargs["pais"], Provincia.nombre == kwargs["provincia"], Ciudad.nombre == kwargs["ciudad"])
			.all()
		)
		return barrios