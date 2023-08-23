from modules.common.gestor_comun import ResponseMessage
from modules.models.entities import Genero
from config import registros_por_pagina
from datetime import datetime

class gestor_generos(ResponseMessage):
	def __init__(self):
		super().__init__()

	def obtener_todo(self):
		return Genero.obtener_todo()
