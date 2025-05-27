from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal


class Bus:

    def get_all_buses(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM buses")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener buses: {e}")
            return []

    def get_by_id(self, bus_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM buses WHERE id_bus = :bus_id")
                result = db.execute(query, {"bus_id": bus_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener bus por ID: {e}")
            return None

    def create_bus(self, numero_bus: str, capacidad: int, estado: int, id_parqueo: int, id_ruta: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO buses (numero_bus, capacidad, estado, id_parqueo, id_ruta)
                    VALUES (:numero_bus, :capacidad, :estado, :id_parqueo, :id_ruta)
                """)
                db.execute(query, {
                    "numero_bus": numero_bus,
                    "capacidad": capacidad,
                    "estado": estado,
                    "id_parqueo": id_parqueo,
                    "id_ruta": id_ruta
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear bus: {e}")
            raise

    def update_bus(self, bus_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
                query = text(f"""
                    UPDATE buses SET {update_fields}
                    WHERE id_bus = :bus_id
                """)
                db.execute(query, {"bus_id": bus_id, **kwargs})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar bus: {e}")
            raise

    def delete_bus(self, bus_id: int):
        try:
            with SessionLocal() as db:
                # Para eliminación lógica, usa:
                # query = text("UPDATE buses SET estado = 0 WHERE id_bus = :bus_id")
                query = text("DELETE FROM buses WHERE id_bus = :bus_id")
                db.execute(query, {"bus_id": bus_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar bus: {e}")
            raise