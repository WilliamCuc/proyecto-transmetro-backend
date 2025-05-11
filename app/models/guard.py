from sqlalchemy.sql import text
from app.db.database import SessionLocal

class Guard:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_guards(self):
        query = text("SELECT * FROM guardias")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_by_id(self, guard_id: int):
        query = text("SELECT * FROM guardias WHERE id_guardia = :guard_id")
        result = self.db.execute(query, {"guard_id": guard_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_guard(self, nombre: str, id_acceso: int):
        query = text("""
            INSERT INTO guardias (nombre, id_acceso)
            VALUES (:nombre, :id_acceso)
        """)
        self.db.execute(query, {
            "nombre": nombre,
            "id_acceso": id_acceso
        })
        self.db.commit()

    def update_guard(self, guard_id: int, **kwargs):
        update_fields = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE guardias SET {update_fields} WHERE id_guardia = :guard_id")
        self.db.execute(query, {"guard_id": guard_id, **kwargs})
        self.db.commit()

    def delete_guard(self, guard_id: int):
        query = text("DELETE FROM guardias WHERE id_guardia = :guard_id")
        self.db.execute(query, {"guard_id": guard_id})
        self.db.commit()