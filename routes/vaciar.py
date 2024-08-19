from flask import Blueprint, jsonify, redirect, url_for
from scripts.vaciar_db import eliminar_todas_las_tablas

vaciar_bp = Blueprint('vaciar', __name__)

@vaciar_bp.route('/vaciar', methods=['GET'])
def vaciar_bd():
    try:
        # Ejecutar la función para eliminar todas las tablas
        eliminar_todas_las_tablas()
        # Redirigir a la página principal con un mensaje de éxito
        return redirect(url_for('main.index'))

    except Exception as e:
        return jsonify({"error": f"Error al vaciar la base de datos: {str(e)}"}), 500
