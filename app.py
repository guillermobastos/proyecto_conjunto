from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noticias.db'  # Usando SQLite para simplicidad
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.String(19), nullable=False)
    impacto = db.Column(db.Float, nullable=False)
    clasificacion = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Noticia {self.titulo}>'

@app.route('/')
def index():
    noticias = Noticia.query.all()
    return render_template('index.html', noticias=noticias)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    df = pd.read_excel(file)
    
    # Reemplaza NaN en la columna 'Descripción' con una cadena vacía
    df['Descripción'].fillna('', inplace=True)
    
    for _, row in df.iterrows():
        noticia = Noticia(
            ticker=row['Ticker'],
            titulo=row['Título'],
            descripcion=row['Descripción'],
            fecha=row['Fecha'],
            impacto=row['Impacto'],
            clasificacion=row['Clasificación']
        )
        db.session.add(noticia)
    
    db.session.commit()
    return 'File successfully uploaded', 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)
