from sqlalchemy.sql import text
from app.db.database import SessionLocal

class Access:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_accesses(self):
        query = text("SELECT * FROM accesos")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_by_id(self, access_id: int):
        query = text("SELECT * FROM accesos WHERE id_acceso = :access_id")
        result = self.db.execute(query, {"access_id": access_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_access(self, descripcion: str, id_estacion: int):
        query = text("""
            INSERT INTO accesos (descripcion, id_estacion)
            VALUES (:descripcion, :id_estacion)
        """)
        self.db.execute(query, {
            "descripcion": descripcion,
            "id_estacion": id_estacion
        })
        self.db.commit()

    def update_access(self, access_id: int, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE accesos SET {update_fields} WHERE id_acceso = :access_id")
        self.db.execute(query, {"access_id": access_id, **kwargs})
        self.db.commit()

    def delete_access(self, access_id: int):
        query = text("DELETE FROM accesos WHERE id_acceso = :access_id")
        self.db.execute(query, {"access_id": access_id})
        self.db.commit()