from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Stop:
    def get_by_id(self, stop_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM paradas WHERE id_parada = :id")
                result = db.execute(query, {"id": stop_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener parada por ID: {e}")
            return None

    def create_stop(self, id_ruta: int, id_estacion: int, orden: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO paradas (id_ruta, id_estacion, orden)
                    VALUES (:id_ruta, :id_estacion, :orden)
                """)
                db.execute(query, {
                    "id_ruta": id_ruta,
                    "id_estacion": id_estacion,
                    "orden": orden
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear parada: {e}")
            raise

    def update_stop(self, stop_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE paradas SET {set_clause} WHERE id_parada = :id")
                kwargs["id"] = stop_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar parada: {e}")
            raise

    def delete_stop(self, stop_id: int):
        try:
            with SessionLocal() as db:
                query = text("DELETE FROM paradas WHERE id_parada = :id")
                db.execute(query, {"id": stop_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar parada: {e}")
            raise

    def get_all_stops(self):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT p.*, r.nombre AS ruta, e.nombre AS estacion
                    FROM paradas p
                    INNER JOIN rutas r ON p.id_ruta = r.id_ruta
                    INNER JOIN estaciones e ON p.id_estacion = e.id_estacion
                """)
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener todas las paradas: {e}")
            return []