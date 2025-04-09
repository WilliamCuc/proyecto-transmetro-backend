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

    def create_user(self, nombre: str, apellido: str, correo: str, contrasena: str, rol: str, estado: bool):
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

    def update_user(self, user_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE usuarios SET {set_clause} WHERE id_usuario = :id")
        kwargs["id"] = user_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_user(self, user_id: int):
        query = text("UPDATE usuarios SET estado = 0 WHERE id_usuario = :id")
        self.db.execute(query, {"id": user_id})
        self.db.commit()