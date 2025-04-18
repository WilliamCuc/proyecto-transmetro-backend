from sqlalchemy import text
from app.db.database import SessionLocal

class Line:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, line_id: int):
        query = text("SELECT * FROM lineas WHERE id_linea = :id")
        result = self.db.execute(query, {"id": line_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_line(self, nombre: str, distancia_total: float, estado: int):
        query = text("""
            INSERT INTO lineas (nombre, distancia_total, estado)
            VALUES (:nombre, :distancia_total, :estado)
        """)
        self.db.execute(query, {
            "nombre": nombre,
            "distancia_total": distancia_total,
            "estado": estado
        })
        self.db.commit()

    def update_line(self, line_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE lineas SET {set_clause} WHERE id_linea = :id")
        kwargs["id"] = line_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_line(self, line_id: int):
        query = text("UPDATE lineas SET estado = 0 WHERE id_linea = :id")
        self.db.execute(query, {"id": line_id})
        self.db.commit()

    def get_all_lines(self):
        query = text("SELECT * FROM lineas")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]