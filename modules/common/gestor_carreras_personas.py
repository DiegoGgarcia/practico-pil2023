from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, personasCarreras, Carrera, Universidad, Facultad, Campus, Programa, TipoPersona, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_

class gestor_carreras_personas(ResponseMessage):
	def __init__(self):
		super().__init__()

	def obtener_carreras_por_persona(self, persona):
		carreras = (
			db.session.query(personasCarreras)
			.filter(personasCarreras.persona==persona)
			.filter(personasCarreras.activo==True)
			.all()
		)
		return carreras
	
	def obtener_pagina(self, pagina, **kwargs):
		query = personasCarreras.query
		if 'persona' in kwargs:
			query = query.filter(personasCarreras.persona == kwargs['persona'])
		carreras, total_paginas = personasCarreras.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas
	
	def eliminar(self, id):
		carrera = personasCarreras.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()
		resultado_borrar=carrera.activar(False)
		self.Exito=resultado_borrar["Exito"]
		self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
		return self.obtenerResultado()

	def asignar_carrera(self, **kwargs):
		if 'universidad' in kwargs:
			universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
		if 'facultad' in kwargs:
			facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
		if 'campus' in kwargs:
			campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
		if 'programa' in kwargs:
			programa=Programa.crear_y_obtener(nombre=kwargs['programa'])
		if 'rol' in kwargs:
			tipopersona=TipoPersona.crear_y_obtener(nombre=kwargs['rol'])
		if 'id_persona' in kwargs:
			persona=Persona.query.get(kwargs['id_persona'])

		carrera=Carrera.crear_y_obtener(universidad=universidad, facultad=facultad, campus=campus, programa=programa)
		persona_carrera=personasCarreras.crear_y_obtener(persona=persona,carrera=carrera,tipopersona=tipopersona)
		
		resultado_guardar=persona_carrera.guardar()
		self.Exito=resultado_guardar["Exito"]
		self.MensajePorFallo=resultado_guardar["MensajePorFallo"]
		return self.obtenerResultado()
