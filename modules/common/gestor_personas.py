from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_, func

class gestor_personas(ResponseMessage):
	def __init__(self):
		super().__init__()
	
	campos_obligatorios = {
		'nombre': 'El nombre es obligatorio',
		'apellido': 'El apellido es obligatorio',
		'personal_id': 'La identificación de la persona es obligatoria',
		'genero': 'El género es obligatorio',
		'pais': 'El país es obligatorio',
		'provincia': 'La provincia es obligatoria',
		'ciudad': 'La ciudad es obligatoria',
		'barrio': 'El barrio es obligatorio',
		'email': 'El email es obligatorio',
		'birthdate': 'La fecha de nacimiento es obligatoria'
	}

	def _validar_campos_obligatorios(self, kwargs):
		for campo, mensaje in self.campos_obligatorios.items():
			if campo not in kwargs or kwargs[campo]=='':
				self.Exito = False
				self.MensajePorFallo = mensaje
				return False
		return True

	def _validar_email(self, email):
		if not validaciones.validar_estructura_email(email):
			self.Exito = False
			self.MensajePorFallo = "El email tiene una estructura no válida."
			return False
		persona_existente = Persona.query.filter_by(email=email).first()
		if persona_existente:
			self.Exito = False
			self.MensajePorFallo = "El email ya está en uso"
			return False
		return True

	def _validar_birthdate(self, birthdate):
		try:
			datetime.strptime(birthdate, '%d-%m-%Y')
			return True
		except ValueError:
			self.Exito = False
			self.MensajePorFallo = "Fecha de nacimiento inválida"
			return False
	
	def obtener_pagina(self, pagina, **kwargs):
		query = Persona.query
		if 'nombre' in kwargs:
			query = query.filter(Persona.nombre.ilike(f"%{kwargs['nombre']}%"))
		if 'apellido' in kwargs:
			query = query.filter(Persona.apellido.ilike(f"%{kwargs['apellido']}%"))
		if 'personal_id' in kwargs:
			query = query.filter(Persona.personal_id.ilike(f"%{kwargs['personal_id']}%"))
		if 'email' in kwargs:
			query = query.filter(Persona.email.ilike(f"%{kwargs['email']}%"))
		if 'genero' in kwargs:
			query = query.join(Genero).filter(Genero.nombre == kwargs['genero'])
		if 'pais' in kwargs:
			query = query.join(Lugar).join(Pais).filter(Pais.nombre.ilike(f"%{kwargs['pais']}%"))
		if 'provincia' in kwargs:
			query = query.join(Lugar).join(Provincia).filter(Provincia.nombre.ilike(f"%{kwargs['provincia']}%"))
		if 'ciudad' in kwargs:
			query = query.join(Lugar).join(Ciudad).filter(Ciudad.nombre.ilike(f"%{kwargs['ciudad']}%"))
		if 'barrio' in kwargs:
			query = query.join(Lugar).join(Barrio).filter(Barrio.nombre.ilike(f"%{kwargs['barrio']}%"))

		personas, total_paginas = Persona.obtener_paginado(query, pagina, registros_por_pagina)
		return personas, total_paginas

	def obtener(self, id):
		persona = Persona.query.get(id)
		if persona==None:
			self.Exito = False
			self.MensajePorFallo = "La persona no existe"
			return self.obtenerResultado()
		self.Resultado = persona
		return self.obtenerResultado()
	
	def editar(self, id, **kwargs):
		persona = Persona.query.get(id)
		if persona==None:
			self.Exito = False
			self.MensajePorFallo = "La persona no existe"
			return self.obtenerResultado()
		
		#Validaciones
		for campo, mensaje in self.campos_obligatorios.items():
			if campo in kwargs and kwargs[campo]=='':
				self.Exito = False
				self.MensajePorFallo = mensaje
				return self.obtenerResultado()
			
		if 'email' in kwargs:
			new_email = kwargs['email']
			if new_email != persona.email:
				if not self._validar_email(new_email):
					return self.obtenerResultado()
				persona.email = new_email

		if 'birthdate' in kwargs:
			new_birthdate = kwargs['birthdate']
			if not self._validar_birthdate(new_birthdate):
				return self.obtenerResultado()
			persona.birthdate = datetime.strptime(new_birthdate, '%d-%m-%Y').isoformat()

		pais=persona.lugar.pais
		provincia=persona.lugar.provincia
		ciudad=persona.lugar.ciudad
		barrio=persona.lugar.barrio

		if 'pais' in kwargs:
			pais=Pais.crear_y_obtener(nombre=kwargs['pais'])
		if 'provincia' in kwargs:
			provincia=Provincia.crear_y_obtener(nombre=kwargs['provincia'])
		if 'ciudad' in kwargs:
			ciudad=Ciudad.crear_y_obtener(nombre=kwargs['ciudad'])
		if 'barrio' in kwargs:
			barrio=Barrio.crear_y_obtener(nombre=kwargs['barrio'])
		lugar=Lugar.crear_y_obtener(pais=pais,provincia=provincia,ciudad=ciudad, barrio=barrio)

		genero=persona.genero
		if 'genero' in kwargs:
			genero=Genero.crear_y_obtener(nombre=kwargs['genero'])

		if 'nombre' in kwargs:
			persona.nombre=kwargs['nombre']
		
		if 'apellido' in kwargs:
			persona.apellido=kwargs['apellido']

		if 'personal_id' in kwargs:
			persona.personal_id=kwargs['personal_id']

		persona.genero=genero
		persona.lugar=lugar

		resultado_guardar=persona.guardar()
		self.Exito=resultado_guardar["Exito"]
		self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

		return self.obtenerResultado()
		
	def eliminar(self, id):
		persona = Persona.query.get(id)
		if persona==None:
			self.Exito = False
			self.MensajePorFallo = "La persona no existe"
			return self.obtenerResultado()
		resultado_borrar=persona.activar(False)
		self.Exito=resultado_borrar["Exito"]
		self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
		return self.obtenerResultado()

	def crear(self, **kwargs):
		if not self._validar_campos_obligatorios(kwargs):
			return self.obtenerResultado()
		
		#Validaciones
		new_email = kwargs['email']
		if not self._validar_email(new_email):
			return self.obtenerResultado()

		new_birthdate = kwargs['birthdate']
		if not self._validar_birthdate(kwargs['birthdate']):
			return self.obtenerResultado()

		genero=Genero.crear_y_obtener(nombre=kwargs['genero'])
		pais=Pais.crear_y_obtener(nombre=kwargs['pais'])
		provincia=Provincia.crear_y_obtener(nombre=kwargs['provincia'])
		ciudad=Ciudad.crear_y_obtener(nombre=kwargs['ciudad'])
		barrio=Barrio.crear_y_obtener(nombre=kwargs['barrio'])
		lugar=Lugar.crear_y_obtener(pais=pais,provincia=provincia,ciudad=ciudad, barrio=barrio)

		nombre = kwargs['nombre']
		apellido = kwargs['apellido']
		email = new_email
		birthdate = datetime.strptime(new_birthdate, '%d-%m-%Y').isoformat()
		personal_id = kwargs['personal_id']

		nueva_persona = Persona(nombre=nombre, apellido=apellido, email=email, birthdate=birthdate, personal_id=personal_id, genero=genero, lugar=lugar)
	
		resultado_crear=nueva_persona.guardar()
		self.Resultado=resultado_crear["Resultado"]
		self.Exito=resultado_crear["Exito"]
		self.MensajePorFallo=resultado_crear["MensajePorFallo"]

		return self.obtenerResultado()
	def obtener_todo(self):
		return Persona.query.all()
	
	def obtener_con_filtro(self, **kwargs):
		query = Persona.query.filter(Persona.activo==True)
		if 'nombre' in kwargs:
			query = query.filter(Persona.nombre.ilike(f"%{kwargs['nombre']}%"))
		if 'apellido' in kwargs:
			query = query.filter(Persona.apellido.ilike(f"%{kwargs['apellido']}%"))
		if 'personal_id' in kwargs:
			query = query.filter(func.replace(Persona.personal_id, '.', '').ilike(f"%{kwargs['personal_id']}%"))
		if 'email' in kwargs:
			query = query.filter(Persona.email.ilike(f"%{kwargs['email']}%"))
		if 'genero' in kwargs:
			query = query.join(Genero).filter(Genero.nombre == kwargs['genero'])
		if 'pais' in kwargs:
			query = query.join(Lugar).join(Pais).filter(Pais.nombre.ilike(f"%{kwargs['pais']}%"))
		if 'provincia' in kwargs:
			query = query.join(Lugar).join(Provincia).filter(Provincia.nombre.ilike(f"%{kwargs['provincia']}%"))
		if 'ciudad' in kwargs:
			query = query.join(Lugar).join(Ciudad).filter(Ciudad.nombre.ilike(f"%{kwargs['ciudad']}%"))
		if 'barrio' in kwargs:
			query = query.join(Lugar).join(Barrio).filter(Barrio.nombre.ilike(f"%{kwargs['barrio']}%"))

		return query.all() if any(kwargs.values()) else []