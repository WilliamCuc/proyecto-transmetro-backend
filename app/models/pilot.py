from sqlalchemy.sql import text
from app.db.database import SessionLocal


class Pilot:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_pilots(self):
        query = text("SELECT * FROM pilotos")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_by_id(self, pilot_id: int):
        query = text("SELECT * FROM pilotos WHERE id_piloto = :pilot_id")
        result = self.db.execute(query, {"pilot_id": pilot_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_pilot(self, nombre: str, historial_educativo: str, direccion: str, telefono: str, id_bus: int):
        query = text("""
            INSERT INTO pilotos (nombre, historial_educativo, direccion, telefono, id_bus)
            VALUES (:nombre, :historial_educativo, :direccion, :telefono, :id_bus)
        """)
        self.db.execute(query, {
            "nombre": nombre,
            "historial_educativo": historial_educativo,
            "direccion": direccion,
            "telefono": telefono,
            "id_bus": id_bus
        })
        self.db.commit()

    def update_pilot(self, pilot_id: int, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE pilotos SET {update_fields} WHERE id_piloto = :pilot_id")
        self.db.execute(query, {"pilot_id": pilot_id, **kwargs})
        self.db.commit()

    def delete_pilot(self, pilot_id: int):
        query = text("DELETE FROM pilotos WHERE id_piloto = :pilot_id")
        self.db.execute(query, {"pilot_id": pilot_id})
        self.db.commit()