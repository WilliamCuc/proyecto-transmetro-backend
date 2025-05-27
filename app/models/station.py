from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Station:
    def get_all_stations(self):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT a.*, b.nombre AS municipio, c.id_departamento, c.nombre AS departamento 
                    FROM estaciones a
                    INNER JOIN municipios b ON a.id_municipio = b.id_municipio
                    INNER JOIN departamentos c ON b.id_departamento = c.id_departamento
                """)
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener estaciones: {e}")
            return []

    def get_by_id(self, station_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM estaciones WHERE id_estacion = :id")
                result = db.execute(query, {"id": station_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener estación por ID: {e}")
            return None

    def create_station(self, nombre: str, ubicacion: str, id_municipio: int, id_linea: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO estaciones (nombre, ubicacion, id_municipio, id_linea)
                    VALUES (:nombre, :ubicacion, :id_municipio, :id_linea)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "ubicacion": ubicacion,
                    "id_municipio": id_municipio,
                    "id_linea": id_linea
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear estación: {e}")
            raise

    def update_station(self, station_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE estaciones SET {set_clause} WHERE id_estacion = :id")
                kwargs["id"] = station_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar estación: {e}")
            raise

    def delete_station(self, station_id: int):
        try:
            with SessionLocal() as db:
                query = text("UPDATE estaciones SET estado = 0 WHERE id_estacion = :id")
                db.execute(query, {"id": station_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar estación (soft delete): {e}")
            raise