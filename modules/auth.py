from flask import redirect, url_for, request, flash, render_template, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules.models.entities import User
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import create_access_token, jwt_required
from flask_wtf.csrf import CSRFProtect
from functools import wraps

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
csrf = CSRFProtect()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    if "/api/" in request.path:
        return abort(401)
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash("Credenciales no válidas. Intente nuevamente.", 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/login-jwt', methods=['POST']) 
@csrf.exempt
def login_jwt():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
  
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg":"Credenciales inválidas"}),401

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def jwt_or_login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                jwt_required()(lambda: None)()
            except:
                if current_user.is_authenticated:
                    return f(*args, **kwargs)
                return {"message": "Acceso no autorizado"}, 401
            return f(*args, **kwargs)

        return decorated_function
    return decorator
