from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class User:
    def get_by_id(self, user_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM usuarios WHERE id_usuario = :id")
                result = db.execute(query, {"id": user_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None

    def create_user(self, nombre: str, apellido: str, correo: str, contrasena: str, rol: str, estado: int):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO usuarios (nombre, apellido, correo, contrasena, rol, estado)
                    VALUES (:nombre, :apellido, :correo, :contrasena, :rol, :estado)
                """)
                db.execute(query, {
                    "nombre": nombre,
                    "apellido": apellido,
                    "correo": correo,
                    "contrasena": contrasena,
                    "rol": rol,
                    "estado": estado
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear usuario: {e}")
            raise

    def update_user(self, user_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE usuarios SET {set_clause} WHERE id_usuario = :id")
                kwargs["id"] = user_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar usuario: {e}")
            raise

    def delete_user(self, user_id: int):
        try:
            with SessionLocal() as db:
                query = text("UPDATE usuarios SET estado = 0 WHERE id_usuario = :id")
                db.execute(query, {"id": user_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar usuario: {e}")
            raise

    def get_all_users(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM usuarios")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los usuarios: {e}")
            return []

    def login(self, correo: str, contrasena: str):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT * FROM usuarios 
                    WHERE correo = :correo AND contrasena = :contrasena AND estado = 1
                """)
                result = db.execute(query, {"correo": correo, "contrasena": contrasena}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error en login de usuario: {e}")
            return None