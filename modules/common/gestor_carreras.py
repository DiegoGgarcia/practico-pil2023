from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Carrera, Universidad, Facultad, Campus, Programa, TipoPersona, db


class gestor_carreras(ResponseMessage):
	def __init__(self):
		super().__init__()

	def obtener_universidades(self):
		return db.session.query(Universidad).distinct().join(Carrera).all()
	

	def obtener_facultades(self, **kwargs):
		resultado = (
			db.session.query(Facultad)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.all()
		)
		return resultado
	
	def obtener_campus(self, **kwargs):
		resultado = (
			db.session.query(Campus)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.filter(Facultad.nombre == kwargs["facultad"])
			.all()
		)
		return resultado

	def obtener_programas(self, **kwargs):
		resultado = (
			db.session.query(Programa)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.join(Campus)
			.filter(Universidad.nombre == kwargs["universidad"])
			.filter(Facultad.nombre == kwargs["facultad"])
			.filter(Campus.nombre == kwargs["campus"])
			.all()
		)
		return resultado

	def obtener_roles(self, **kwargs):
		resultado = (
			db.session.query(TipoPersona).all()
		)
		return resultado
	

