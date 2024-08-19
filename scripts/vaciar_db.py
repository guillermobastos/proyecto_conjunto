from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError

# Configuración de la base de datos
DATABASE_URI = 'sqlite:///database/noticias.db'
engine = create_engine(DATABASE_URI)
metadata = MetaData()

def eliminar_todas_las_tablas():
    """Elimina todas las tablas en la base de datos especificada."""
    try:
        # Conectar a la base de datos
        with engine.connect() as conn:
            # Reflejar las tablas existentes en el metadata
            metadata.reflect(bind=engine)
            
            # Obtener una lista de todas las tablas
            tablas = metadata.tables.keys()
            
            if not tablas:
                print("No hay tablas en la base de datos para eliminar.")
                return
            
            # Eliminar cada tabla
            for tabla in tablas:
                table = metadata.tables[tabla]
                table.drop(bind=engine)
                print(f"Tabla {tabla} eliminada.")
                
            print("Todas las tablas han sido eliminadas.")
            
    except SQLAlchemyError as e:
        print(f"Error al eliminar las tablas: {e}")

if __name__ == "__main__":
    eliminar_todas_las_tablas()
