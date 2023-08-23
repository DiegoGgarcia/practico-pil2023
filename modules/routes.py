from flask import Blueprint, render_template, redirect, url_for, session,flash
from flask_login import login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from modules.models.entities import Persona
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
@login_required
def about():
    return render_template('about.html')

@routes_bp.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        flash('Formulario enviado con éxito', 'success')
        return redirect(url_for('routes.index')) 

    return render_template('contact.html', form=form)

@routes_bp.route('/calificaciones')
@login_required
def calificaciones():
    return render_template('calificaciones.html')
