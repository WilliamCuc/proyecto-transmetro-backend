from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Access:

    def get_all_accesses(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM accesos")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener accesos: {e}")
            return []

    def get_by_id(self, access_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM accesos WHERE id_acceso = :access_id")
                result = db.execute(query, {"access_id": access_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener acceso por ID: {e}")
            return None

    def create_access(self, descripcion: str, id_estacion: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO accesos (descripcion, id_estacion)
                    VALUES (:descripcion, :id_estacion)
                """)
                db.execute(query, {
                    "descripcion": descripcion,
                    "id_estacion": id_estacion
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear acceso: {e}")
            raise

    def update_access(self, access_id: int, **kwargs):
        if not kwargs:
            return  # Nada que actualizar
        try:
            with SessionLocal() as db:
                update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
                query = text(f"""
                    UPDATE accesos SET {update_fields}
                    WHERE id_acceso = :access_id
                """)
                db.execute(query, {"access_id": access_id, **kwargs})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar acceso: {e}")
            raise

    def delete_access(self, access_id: int):
        try:
            with SessionLocal() as db:
                # Si prefieres eliminación lógica, usa:
                # query = text("UPDATE accesos SET estado = 0 WHERE id_acceso = :access_id")
                query = text("DELETE FROM accesos WHERE id_acceso = :access_id")
                db.execute(query, {"access_id": access_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar acceso: {e}")
            raise