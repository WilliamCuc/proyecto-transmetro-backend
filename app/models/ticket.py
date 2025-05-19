from sqlalchemy import text
from app.db.database import SessionLocal

class Ticket:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, ticket_id: int):
        query = text("SELECT * FROM boletos WHERE id_boleto = :id")
        result = self.db.execute(query, {"id": ticket_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_ticket(self, id_usuario: int, id_ruta: int, fecha_compra: str, precio: float):
        query = text("""
            INSERT INTO boletos (id_usuario, id_ruta, fecha_compra, precio)
            VALUES (:id_usuario, :id_ruta, :fecha_compra, :precio)
        """)
        self.db.execute(query, {
            "id_usuario": id_usuario,
            "id_ruta": id_ruta,
            "fecha_compra": fecha_compra,
            "precio": precio
        })
        self.db.commit()

    def update_ticket(self, ticket_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE boletos SET {set_clause} WHERE id_boleto = :id")
        kwargs["id"] = ticket_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_ticket(self, ticket_id: int):
        query = text("DELETE FROM boletos WHERE id_boleto = :id")
        self.db.execute(query, {"id": ticket_id})
        self.db.commit()

    def get_all_tickets(self):
        query = text("""
            SELECT b.*, u.nombre AS usuario, r.nombre AS ruta
            FROM boletos b
            INNER JOIN usuarios u ON b.id_usuario = u.id_usuario
            INNER JOIN rutas r ON b.id_ruta = r.id_ruta
        """)
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]