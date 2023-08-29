from modules.common.gestor_comun import ResponseMessage
from modules.models.entities import Genero

class gestor_generos(ResponseMessage):
	def __init__(self):
		super().__init__()

	def obtener_todo(self):
		return Genero.obtener_todo()
