from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Parking:

    def get_all_parkings(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM parqueos")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener parqueos: {e}")
            return []

    def get_by_id(self, parking_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM parqueos WHERE id_parqueo = :parking_id")
                result = db.execute(query, {"parking_id": parking_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener parqueo por ID: {e}")
            return None

    def create_parking(self, id_estacion: int, codigo: str):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO parqueos (id_estacion, codigo)
                    VALUES (:id_estacion, :codigo)
                """)
                db.execute(query, {
                    "id_estacion": id_estacion,
                    "codigo": codigo
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear parqueo: {e}")
            raise

    def update_parking(self, parking_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
                query = text(f"""
                    UPDATE parqueos
                    SET {update_fields}
                    WHERE id_parqueo = :parking_id
                """)
                db.execute(query, {"parking_id": parking_id, **kwargs})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar parqueo: {e}")
            raise

    def delete_parking(self, parking_id: int):
        try:
            with SessionLocal() as db:
                # Elimina físicamente. Si prefieres lógica: SET estado = 0
                query = text("DELETE FROM parqueos WHERE id_parqueo = :parking_id")
                db.execute(query, {"parking_id": parking_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar parqueo: {e}")
            raise