from flask import Blueprint, jsonify, redirect, url_for
from scripts.main_threads import main

ejecutar_bp = Blueprint('ejecutar', __name__)

@ejecutar_bp.route('/ejecutar', methods=['GET'])
def ejecutar_script():
    try:
        # Ejecutar la función del script
        resultado = main()
        
        return redirect(url_for('main.index'))
    except Exception as e:
        return jsonify({"error": f"Error al ejecutar el script: {str(e)}"}), 500
