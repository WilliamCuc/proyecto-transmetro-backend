from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Route:
    def get_by_id(self, route_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM rutas WHERE id_ruta = :id")
                result = db.execute(query, {"id": route_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error getting route by ID: {e}")
            return None

    def create_route(self, nombre: str, descripcion: str, id_linea: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO rutas (nombre, descripcion, id_linea)
                    VALUES (:nombre, :descripcion, :id_linea)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "id_linea": id_linea
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error creating route: {e}")
            raise

    def update_route(self, route_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE rutas SET {set_clause} WHERE id_ruta = :id")
                kwargs["id"] = route_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error updating route: {e}")
            raise

    def delete_route(self, route_id: int):
        try:
            with SessionLocal() as db:
                query = text("DELETE FROM rutas WHERE id_ruta = :id")
                db.execute(query, {"id": route_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error deleting route: {e}")
            raise

    def get_all_routes(self):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT r.*, l.nombre AS linea
                    FROM rutas r
                    INNER JOIN lineas l ON r.id_linea = l.id_linea
                """)
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error getting all routes: {e}")
            return []