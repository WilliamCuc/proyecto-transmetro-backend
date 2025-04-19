from sqlalchemy import text
from app.db.database import SessionLocal

class Route:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, route_id: int):
        query = text("SELECT * FROM rutas WHERE id_ruta = :id")
        result = self.db.execute(query, {"id": route_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_route(self, nombre: str, descripcion: str, id_linea: int):
        query = text("""
            INSERT INTO rutas (nombre, descripcion, id_linea)
            VALUES (:nombre, :descripcion, :id_linea)
        """)
        self.db.execute(query, {
            "nombre": nombre,
            "descripcion": descripcion,
            "id_linea": id_linea
        })
        self.db.commit()

    def update_route(self, route_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE rutas SET {set_clause} WHERE id_ruta = :id")
        kwargs["id"] = route_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_route(self, route_id: int):
        query = text("DELETE FROM rutas WHERE id_ruta = :id")
        self.db.execute(query, {"id": route_id})
        self.db.commit()

    def get_all_routes(self):
        query = text("""
            SELECT r.*, l.nombre AS linea
            FROM rutas r
            INNER JOIN lineas l ON r.id_linea = l.id_linea
        """)
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]