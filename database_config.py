# # database_config.py

# from sqlalchemy import create_engine, MetaData

# # Configuración de la base de datos
# DATABASE_URI = "sqlite:///database/noticias.db"
# engine = create_engine(DATABASE_URI)
# metadata = MetaData()


# from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, Text, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

# # Definir la tabla predicciones
# class Predicciones(Base):
#     __tablename__ = 'predicciones'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     ticker = Column(String(10), nullable=False)
#     fecha = Column(TIMESTAMP, nullable=False)
#     prediccion = Column(Float, nullable=False)
#     clasificacion = Column(Integer, nullable=False)
#     descripcion = Column(Text, nullable=True)

# # Crear las tablas en la base de datos
# Base.metadata.create_all(engine)
# # Crear una sesión
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker  # Usar el import correcto

# Configuración de la base de datos
DATABASE_URI = "sqlite:///database/noticias.db"
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Definir la clase base usando declarative_base() desde sqlalchemy.orm
Base = declarative_base()

# Definir la tabla predicciones
class Predicciones(Base):
    __tablename__ = 'predicciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    prediccion = Column(Float, nullable=False)
    clasificacion = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
