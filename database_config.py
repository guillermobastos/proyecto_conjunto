# database_config.py

from sqlalchemy import create_engine, MetaData

# Configuración de la base de datos
DATABASE_URI = "sqlite:///database/noticias.db"
engine = create_engine(DATABASE_URI)
metadata = MetaData()
