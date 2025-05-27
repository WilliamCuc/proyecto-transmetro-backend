from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal


class Schedule:

    def get_all_schedules(self):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT h.*, r.nombre AS ruta
                    FROM horarios h
                    INNER JOIN rutas r ON h.id_ruta = r.id_ruta
                """)
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener los horarios: {e}")
            return []

    def get_by_id(self, schedule_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM horarios WHERE id_horario = :id")
                result = db.execute(query, {"id": schedule_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener horario por ID: {e}")
            return None

    def create_schedule(self, id_ruta: int, hora_salida: str, hora_llegada: str):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO horarios (id_ruta, hora_salida, hora_llegada)
                    VALUES (:id_ruta, :hora_salida, :hora_llegada)
                """)
                db.execute(query, {
                    "id_ruta": id_ruta,
                    "hora_salida": hora_salida,
                    "hora_llegada": hora_llegada
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear horario: {e}")
            raise

    def update_schedule(self, schedule_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"""
                    UPDATE horarios
                    SET {set_clause}
                    WHERE id_horario = :id
                """)
                kwargs["id"] = schedule_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar horario: {e}")
            raise

    def delete_schedule(self, schedule_id: int):
        try:
            with SessionLocal() as db:
                query = text("DELETE FROM horarios WHERE id_horario = :id")
                db.execute(query, {"id": schedule_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar horario: {e}")
            raise