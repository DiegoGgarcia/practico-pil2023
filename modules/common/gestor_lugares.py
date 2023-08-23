from modules.common.gestor_comun import ResponseMessage, validaciones
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