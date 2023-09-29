from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
from sqlalchemy import and_
from sqlalchemy.inspection import inspect
from math import ceil
from datetime import datetime

db = SQLAlchemy()

class BaseEntity(db.Model):
	__abstract__ = True

	fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
	fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
	activo = db.Column(db.Boolean, default=True)

	def guardar(self):
		exito=True
		mensaje=""
		try:
			if self.id==None:
				db.session.add(self)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":self, "Exito":exito, "MensajePorFallo":mensaje}

	def borrar(self):
		exito=True
		mensaje=""
		try:
			db.session.delete(self)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":None, "Exito":exito, "MensajePorFallo":mensaje}

	def activar(self, estado):
		exito=True
		mensaje=""
		try:
			self.activo=estado
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			exito=False
			mensaje=str(e)
		return {"Resultado":None, "Exito":exito, "MensajePorFallo":mensaje}

	@classmethod
	def crear_y_obtener(cls, **kwargs):
		entidad = db.session.query(cls).filter_by(**kwargs).first()
		if not entidad:
			entidad = cls(**kwargs)
			db.session.add(entidad)
		return entidad
		
	def serialize(self):
		serializable_data = {}
		for column in self.__table__.columns:
			value = getattr(self, column.name)
			if isinstance(value, datetime):
				# Si el valor es de tipo datetime, aplicar isoformat()
				serializable_data[column.name] = value.isoformat()
			else:
				serializable_data[column.name] = value
		return serializable_data
	
	@staticmethod
	def obtener_paginado(query, pagina, items_por_pagina):
		total_objetos = query.count()
		total_paginas = ceil(total_objetos / items_por_pagina)
		objetos = query.paginate(page=pagina, per_page=items_por_pagina)
		return objetos, total_paginas
	
	@classmethod
	def obtener_todo(cls):
		objetos = cls.query.all()
		return objetos