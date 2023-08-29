from flask import Blueprint, render_template, redirect, url_for, session,flash
from flask_login import login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from modules.common.gestor_email import gestor_email 

from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

# Definir el formulario de contacto
class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired()])
    message = StringField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Manejar rutas no válidas
@routes_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@routes_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@routes_bp.route('/index')
@login_required
def index():
    return render_template('index.html')

@routes_bp.route('/about')
def about():
    return render_template('about.html')

@routes_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        nombre = form.name.data
        mensaje_enviado = form.message.data

        mensaje_respuesta= f'Hola {nombre}\nGracias por contactarnos.\n\nSu mensaje:\n{mensaje_enviado}'
        resultado=gestor_email().enviar_email(email,"Formulario de contacto",mensaje_respuesta)
        if resultado["Exito"]:
            flash('Formulario enviado con éxito', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('contact.html', form=form)

