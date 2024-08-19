from flask import Blueprint, jsonify, request
from sqlalchemy import text
from database_config import engine

predicciones_bp = Blueprint('predicciones', __name__)

@predicciones_bp.route('/predicciones', methods=['GET'])
def predicciones():
    ticker = request.args.get('ticker', default=None, type=str)

    if not ticker:
        return jsonify({"error": "Debe proporcionar un ticker en los parámetros de la solicitud."}), 400

    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM predicciones WHERE ticker = :ticker")
            result = conn.execute(query, {"ticker": ticker})
            predicciones = [dict(row) for row in result]

        if not predicciones:
            return jsonify({"mensaje": f"No se encontraron predicciones para el ticker {ticker}."}), 404

        return jsonify(predicciones)

    except Exception as e:
        return jsonify({"error": f"Error al obtener predicciones: {str(e)}"}), 500
