from flask import Flask
from routes.main import main_bp
from routes.predicciones import predicciones_bp
from routes.ejecutar import ejecutar_bp  
from routes.vaciar import vaciar_bp  

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(main_bp)
app.register_blueprint(predicciones_bp)
app.register_blueprint(ejecutar_bp)  
app.register_blueprint(vaciar_bp)

if __name__ == '__main__':
    app.run(debug=True)
