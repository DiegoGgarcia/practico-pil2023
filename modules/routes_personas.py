from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_personas import gestor_personas
from modules.common.gestor_generos import gestor_generos
from flask import Blueprint
from modules.auth import csrf

personas_bp = Blueprint('routes_personas', __name__)

@personas_bp.route('/personas', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    apellido = request.args.get('apellido', default="", type=str)
    email = request.args.get('email', default="", type=str)
    filtros = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email
    }
    personas, total_paginas = gestor_personas().obtener_pagina(page, **filtros)
    return render_template('personas/personas.html', personas=personas, total_paginas=total_paginas, csrf=csrf, filtros=filtros)

@personas_bp.route('/personas/<int:persona_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_persona(persona_id):
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_personas().editar(persona_id, **formulario_data)
        if resultado["Exito"]:
            flash('Persona actualizada correctamente', 'success')
            return redirect(url_for('routes_personas.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')

    resultado=gestor_personas().obtener(persona_id)
    if resultado["Exito"]:
        persona=resultado["Resultado"]
        return render_template('personas/editar_persona.html', persona=persona, csrf=csrf)
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_personas.obtener_lista_paginada'))
    
@personas_bp.route('/personas/<int:persona_id>', methods=['POST'])
@login_required
def eliminar_persona(persona_id):
    resultado=gestor_personas().eliminar(persona_id)
    if resultado["Exito"]:
        flash('Persona eliminada correctamente', 'success')
    else:
        flash('Error al eliminar persona', 'success')
    return redirect(url_for('routes_personas.obtener_lista_paginada'))

@personas_bp.route('/personas/crear', methods=['GET', 'POST'])
@login_required
def crear_persona():
    formulario_data = {} 
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_personas().crear(**formulario_data)
        if resultado["Exito"]:
            flash('Persona creada correctamente', 'success')
            return redirect(url_for('routes_personas.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('personas/crear_persona.html', formulario_data=formulario_data, csrf=csrf)

