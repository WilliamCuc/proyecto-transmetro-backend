from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Guard:

    def get_all_guards(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM guardias")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener guardias: {e}")
            return []

    def get_by_id(self, guard_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM guardias WHERE id_guardia = :guard_id")
                result = db.execute(query, {"guard_id": guard_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener guardia por ID: {e}")
            return None

    def create_guard(self, nombre: str, id_acceso: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO guardias (nombre, id_acceso)
                    VALUES (:nombre, :id_acceso)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "id_acceso": id_acceso
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear guardia: {e}")
            raise

    def update_guard(self, guard_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                update_fields = ", ".join([f"{key} = :{key}" for key in kwargs])
                query = text(f"""
                    UPDATE guardias
                    SET {update_fields}
                    WHERE id_guardia = :guard_id
                """)
                db.execute(query, {"guard_id": guard_id, **kwargs})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar guardia: {e}")
            raise

    def delete_guard(self, guard_id: int):
        try:
            with SessionLocal() as db:
                # Para eliminación lógica, descomenta esta línea:
                # query = text("UPDATE guardias SET estado = 0 WHERE id_guardia = :guard_id")
                query = text("DELETE FROM guardias WHERE id_guardia = :guard_id")
                db.execute(query, {"guard_id": guard_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar guardia: {e}")
            raise