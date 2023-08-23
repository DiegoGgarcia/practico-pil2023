import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from modules.models.base import BaseEntity, db
	
class Persona(BaseEntity):
	__tablename__ = "personas"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100))
	apellido = db.Column(db.String(100))
	email = email = db.Column(db.String(255), unique = True)
	birthdate = db.Column(db.Date)
	personal_id = db.Column(db.String(50), unique = True)
	genero_id = db.Column(db.Integer,db.ForeignKey("genero.id"), nullable=False)
	lugar_id = db.Column(db.Integer, db.ForeignKey("lugar.id"), nullable=False)

	genero = db.relationship("Genero", backref = "related_genero")
	lugar = db.relationship("Lugar", backref = "related_lugar")

	def __init__(self, nombre, apellido, email, birthdate, personal_id, genero, lugar):
		self.nombre = nombre
		self.apellido = apellido
		self.email = email
		self.birthdate = birthdate
		self.personal_id = personal_id
		self.genero = genero
		self.lugar = lugar

	@hybrid_property
	def age(self):
		today = datetime.date.today()
		edad = today.year - self.birthdate.year
		if (today.month, today.day) < (self.birthdate.month, self.birthdate.day):
			edad -= 1
		return edad

	@age.expression
	def age(cls):
		today = datetime.date.today()
		birthdate_year = db.func.extract('year', cls.birthdate)
		birthdate_month = db.func.extract('month', cls.birthdate)
		birthdate_day = db.func.extract('day', cls.birthdate)
		return db.case(
			(
				(
					(birthdate_month < today.month) |
					((birthdate_month == today.month) & (birthdate_day <= today.day)),
					today.year - birthdate_year - 1
				)
			),
			else_=today.year - birthdate_year
		)

class Genero(BaseEntity):
	__tablename__ = "genero"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(50), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class TipoPersona(BaseEntity):
	__tablename__ = "tipopersona"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(50), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Pais(BaseEntity):
	__tablename__ = "pais"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Ciudad(BaseEntity):
	__tablename__ = "ciudad"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Barrio(BaseEntity):
	__tablename__ = "barrio"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Provincia(BaseEntity):
	__tablename__ = "provincia"
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Lugar(BaseEntity):
	__tablename__ = "lugar"
	__table_args__ = (db.UniqueConstraint('pais_id','ciudad_id','barrio_id','provincia_id', name='uidx_sitio_unico'), )
	id = db.Column(db.Integer, primary_key = True)
	pais_id = db.Column(db.Integer, db.ForeignKey("pais.id"), nullable=False)
	ciudad_id = db.Column(db.Integer,db.ForeignKey("ciudad.id"), nullable=False)
	barrio_id = db.Column(db.Integer,db.ForeignKey("barrio.id"), nullable=False)
	provincia_id = db.Column(db.Integer,db.ForeignKey("provincia.id"), nullable=False)

	pais = db.relationship("Pais", backref = "related_pais")
	ciudad = db.relationship("Ciudad", backref = "related_ciudad")
	barrio = db.relationship("Barrio", backref = "related_barrio")
	provincia = db.relationship("Provincia", backref = "related_provincia")

	def __init__(self, pais, ciudad, barrio, provincia):
		self.pais = pais
		self.ciudad = ciudad
		self.barrio = barrio
		self.provincia = provincia

class Programa(BaseEntity):
	__tablename__ = "programa"
	id = db.Column(db.Integer, primary_key = True)	
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Facultad(BaseEntity):
	__tablename__ = "facultad"
	id = db.Column(db.Integer, primary_key = True)	
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Universidad(BaseEntity):
	__tablename__ = "universidad"
	id = db.Column(db.Integer, primary_key = True)	
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Campus(BaseEntity):
	__tablename__ = "campus"
	id = db.Column(db.Integer, primary_key = True)	
	nombre = db.Column(db.String(100), unique = True)

	def __init__(self, nombre):
		self.nombre = nombre

class Carrera(BaseEntity):
	__tablename__ = "carrera"
	__table_args__ = (db.UniqueConstraint('programa_id', 'facultad_id', 'universidad_id','campus_id', name='uix_table_programa_facultad_universidad_campus'),)
	id = db.Column(db.Integer, primary_key = True)
	programa_id = db.Column(db.Integer, db.ForeignKey("programa.id"), nullable=False)
	facultad_id = db.Column(db.Integer, db.ForeignKey("facultad.id"), nullable=False)
	universidad_id = db.Column(db.Integer, db.ForeignKey("universidad.id"), nullable=False)
	campus_id = db.Column(db.Integer, db.ForeignKey("campus.id"), nullable=False)

	programa = db.relationship("Programa", backref = "related_programa")
	facultad = db.relationship("Facultad", backref = "related_facultad")
	universidad = db.relationship("Universidad", backref = "related_universidad")
	campus = db.relationship("Campus", backref = "related_campus")

	def __init__(self, programa, facultad, universidad, campus):
		self.programa = programa
		self.facultad = facultad
		self.universidad = universidad
		self.campus = campus

class personasCarreras(BaseEntity):
	__tablename__ = "personasCarreras"
	__table_args__ = (db.UniqueConstraint('persona_id', 'carrera_id', 'tipo_id', name='uix_pers_carreras_tipo_unico'),)
	id = db.Column(db.Integer, primary_key = True)
	persona_id = db.Column(db.Integer, db.ForeignKey("personas.id"), nullable=False)
	carrera_id = db.Column(db.Integer, db.ForeignKey("carrera.id"), nullable=False)
	tipo_id = db.Column(db.Integer, db.ForeignKey("tipopersona.id"), nullable=False)

	persona = db.relationship("Persona", backref = "related_persona")
	carrera = db.relationship("Carrera", backref = "related_carrera")
	tipopersona = db.relationship("TipoPersona", backref = "related_tipopersona")

	def __init__(self, persona, carrera, tipopersona):
		self.persona = persona
		self.carrera = carrera
		self.tipopersona = tipopersona

class User(BaseEntity,UserMixin):
	__tablename__ = "usuarios"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	persona_id = db.Column(db.Integer, db.ForeignKey("personas.id"))

	persona = db.relationship("Persona", backref="user", uselist=False)

	def __init__(self, username, password):
		self.username = username
		self.set_password(password)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
