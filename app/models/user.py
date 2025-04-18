from sqlalchemy import text
from sqlalchemy.engine import Row
from app.db.database import SessionLocal

class User:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, user_id: int):
        query = text("SELECT * FROM usuarios WHERE id_usuario = :id")
        result = self.db.execute(query, {"id": user_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_user(self, nombre: str, apellido: str, correo: str, contrasena: str, rol: str, estado: int):
        try:
            query = text("""
                INSERT INTO usuarios (nombre, apellido, correo, contrasena, rol, estado)
                VALUES (:nombre, :apellido, :correo, :contrasena, :rol, :estado)
            """)
            self.db.execute(query, {
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "contrasena": contrasena,
                "rol": rol,
                "estado": estado
            })
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def update_user(self, user_id: int, **kwargs):
        try:
            set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
            query = text(f"UPDATE usuarios SET {set_clause} WHERE id_usuario = :id")
            kwargs["id"] = user_id
            self.db.execute(query, kwargs)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def delete_user(self, user_id: int):
        try:
            query = text("UPDATE usuarios SET estado = 0 WHERE id_usuario = :id")
            self.db.execute(query, {"id": user_id})
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_all_users(self):
        try:
            query = text("SELECT * FROM usuarios")
            result = self.db.execute(query).fetchall()
            return [dict(row._mapping) for row in result]
        finally:
            self.db.close()
    
    def login(self, correo: str, contrasena: str):
        try:
            query = text("SELECT * FROM usuarios WHERE correo = :correo AND contrasena = :contrasena")
            result = self.db.execute(query, {"correo": correo, "contrasena": contrasena}).fetchone()
            return dict(result._mapping) if result else None
        finally:
            self.db.close()