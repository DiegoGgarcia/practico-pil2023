from flask_restful import Resource, reqparse
from modules.models.entities import User
from flask_jwt_extended import create_access_token, jwt_required
from functools import wraps

def jwt_or_login_required():
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			try:
				jwt_required()(lambda: None)()
			except:
				return {"message": "Acceso no autorizado"}, 401
			return f(*args, **kwargs)
		return decorated_function
	return decorator

class AuthResource(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('username', type=str, required=True, help='Usuario requerido')
		self.parser.add_argument('password', type=str, required=True, help='Password requerida')

	def post(self):
		args = self.parser.parse_args()
		username = args['username']
		password = args['password']
		user = User.query.filter_by(username=username).first()
		if user and user.check_password(password):
			access_token = create_access_token(identity=username)
			return {"access_token":access_token}, 200
		else:
			return {"msg":"Credenciales inválidas"}, 401
