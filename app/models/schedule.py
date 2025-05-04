from sqlalchemy import text
from app.db.database import SessionLocal

class Schedule:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, schedule_id: int):
        query = text("SELECT * FROM horarios WHERE id_horario = :id")
        result = self.db.execute(query, {"id": schedule_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_schedule(self, id_ruta: int, hora_salida: str, hora_llegada: str):
        query = text("""
            INSERT INTO horarios (id_ruta, hora_salida, hora_llegada)
            VALUES (:id_ruta, :hora_salida, :hora_llegada)
        """)
        self.db.execute(query, {
            "id_ruta": id_ruta,
            "hora_salida": hora_salida,
            "hora_llegada": hora_llegada
        })
        self.db.commit()

    def update_schedule(self, schedule_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE horarios SET {set_clause} WHERE id_horario = :id")
        kwargs["id"] = schedule_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_schedule(self, schedule_id: int):
        query = text("DELETE FROM horarios WHERE id_horario = :id")
        self.db.execute(query, {"id": schedule_id})
        self.db.commit()

    def get_all_schedules(self):
        query = text("""
            SELECT h.*, r.nombre AS ruta
            FROM horarios h
            INNER JOIN rutas r ON h.id_ruta = r.id_ruta
        """)
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]