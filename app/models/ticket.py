from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Ticket:
    def get_by_id(self, ticket_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM boletos WHERE id_boleto = :id")
                result = db.execute(query, {"id": ticket_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener boleto por ID: {e}")
            return None

    def create_ticket(self, id_usuario: int, id_ruta: int, fecha_compra: str, precio: float):
        try:
            with SessionLocal() as db:
                query = text("""
                    INSERT INTO boletos (id_usuario, id_ruta, fecha_compra, precio)
                    VALUES (:id_usuario, :id_ruta, :fecha_compra, :precio)
                """)
                db.execute(query, {
                    "id_usuario": id_usuario,
                    "id_ruta": id_ruta,
                    "fecha_compra": fecha_compra,
                    "precio": precio
                })
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al crear boleto: {e}")
            raise

    def update_ticket(self, ticket_id: int, **kwargs):
        if not kwargs:
            return
        try:
            with SessionLocal() as db:
                set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
                query = text(f"UPDATE boletos SET {set_clause} WHERE id_boleto = :id")
                kwargs["id"] = ticket_id
                db.execute(query, kwargs)
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al actualizar boleto: {e}")
            raise

    def delete_ticket(self, ticket_id: int):
        try:
            with SessionLocal() as db:
                query = text("DELETE FROM boletos WHERE id_boleto = :id")
                db.execute(query, {"id": ticket_id})
                db.commit()
        except SQLAlchemyError as e:
            print(f"Error al eliminar boleto: {e}")
            raise

    def get_all_tickets(self):
        try:
            with SessionLocal() as db:
                query = text("""
                    SELECT b.*, u.nombre AS usuario, r.nombre AS ruta
                    FROM boletos b
                    INNER JOIN usuarios u ON b.id_usuario = u.id_usuario
                    INNER JOIN rutas r ON b.id_ruta = r.id_ruta
                """)
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los boletos: {e}")
            return []