from sqlalchemy.sql import text
from app.db.database import SessionLocal


class Parking:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_parkings(self):
        query = text("SELECT * FROM parqueos")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_by_id(self, parking_id: int):
        query = text("SELECT * FROM parqueos WHERE id_parqueo = :parking_id")
        result = self.db.execute(query, {"parking_id": parking_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_parking(self, id_estacion: int, codigo: str):
        query = text("INSERT INTO parqueos (id_estacion, codigo) VALUES (:id_estacion, :codigo)")
        self.db.execute(query, {"id_estacion": id_estacion, "codigo": codigo})
        self.db.commit()

    def update_parking(self, parking_id: int, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE parqueos SET {update_fields} WHERE id_parqueo = :parking_id")
        self.db.execute(query, {"parking_id": parking_id, **kwargs})
        self.db.commit()

    def delete_parking(self, parking_id: int):
        query = text("DELETE FROM parqueos WHERE id_parqueo = :parking_id")
        self.db.execute(query, {"parking_id": parking_id})
        self.db.commit()