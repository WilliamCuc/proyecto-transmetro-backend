from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Line:

    def get_by_id(self, line_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM lineas WHERE id_linea = :id")
                result = db.execute(query, {"id": line_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener línea: {e}")
            return None

    def create_line(self, nombre: str, distancia_total: float, estado: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO lineas (nombre, distancia_total, estado)
                    VALUES (:nombre, :distancia_total, :estado)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "distancia_total": distancia_total,
                    "estado": estado
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear línea: {e}")
            raise

    def update_line(self, line_id: int, **kwargs):
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE lineas SET {set_clause} WHERE id_linea = :id")
                kwargs["id"] = line_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar línea: {e}")
            raise

    def delete_line(self, line_id: int):
        try:
            with SessionLocal() as db:
                query = text("UPDATE lineas SET estado = 0 WHERE id_linea = :id")
                db.execute(query, {"id": line_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar línea: {e}")
            raise

    def get_all_lines(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM lineas")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener líneas: {e}")
            return []