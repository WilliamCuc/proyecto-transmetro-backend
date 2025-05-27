from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal


class Pilot:

    def get_all_pilots(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM pilotos")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener pilotos: {e}")
            return []

    def get_by_id(self, pilot_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM pilotos WHERE id_piloto = :pilot_id")
                result = db.execute(query, {"pilot_id": pilot_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener piloto por ID: {e}")
            return None

    def create_pilot(self, nombre: str, historial_educativo: str, direccion: str, telefono: str, id_bus: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO pilotos (nombre, historial_educativo, direccion, telefono, id_bus)
                    VALUES (:nombre, :historial_educativo, :direccion, :telefono, :id_bus)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "historial_educativo": historial_educativo,
                    "direccion": direccion,
                    "telefono": telefono,
                    "id_bus": id_bus
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear piloto: {e}")
            raise

    def update_pilot(self, pilot_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
                query = text(f"""
                    UPDATE pilotos
                    SET {update_fields}
                    WHERE id_piloto = :pilot_id
                """)
                db.execute(query, {"pilot_id": pilot_id, **kwargs})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar piloto: {e}")
            raise

    def delete_pilot(self, pilot_id: int):
        try:
            with SessionLocal() as db:
                query = text("DELETE FROM pilotos WHERE id_piloto = :pilot_id")
                db.execute(query, {"pilot_id": pilot_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar piloto: {e}")
            raise