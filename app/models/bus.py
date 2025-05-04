from sqlalchemy.sql import text
from app.db.database import SessionLocal


class Bus:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_buses(self):
        query = text("SELECT * FROM buses")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_by_id(self, bus_id: int):
        query = text("SELECT * FROM buses WHERE id_bus = :bus_id")
        result = self.db.execute(query, {"bus_id": bus_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_bus(self, numero_bus: str, capacidad: int, estado: str, id_parqueo: int):
        query = text("""
            INSERT INTO buses (numero_bus, capacidad, estado, id_parqueo)
            VALUES (:numero_bus, :capacidad, :estado, :id_parqueo)
        """)
        self.db.execute(query, {
            "numero_bus": numero_bus,
            "capacidad": capacidad,
            "estado": estado,
            "id_parqueo": id_parqueo
        })
        self.db.commit()

    def update_bus(self, bus_id: int, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE buses SET {update_fields} WHERE id_bus = :bus_id")
        self.db.execute(query, {"bus_id": bus_id, **kwargs})
        self.db.commit()

    def delete_bus(self, bus_id: int):
        query = text("DELETE FROM buses WHERE id_bus = :bus_id")
        self.db.execute(query, {"bus_id": bus_id})
        self.db.commit()