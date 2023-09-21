from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, personasCarreras, Carrera, Universidad, Facultad, Campus, Programa, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_

class gestor_carreras_personas(ResponseMessage):
	def __init__(self):
		super().__init__()

	def obtener_carreras_por_persona(persona):
		carreras = (
			db.session.query(personasCarreras).filter(personasCarreras.persona==persona)
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.join(Campus)
			.join(Programa)
			.order_by(Universidad.nombre, Facultad.nombre, Campus.nombre, Programa.nombre).all()
		)
		return carreras
	
	def obtener_pagina(self, pagina, **kwargs):
		query = personasCarreras.query
		if 'persona' in kwargs:
			query = query.filter(personasCarreras.persona == kwargs['persona'])
		carreras, total_paginas = personasCarreras.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas