from sqlalchemy import text
from app.db.database import SessionLocal

class Stop:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, stop_id: int):
        query = text("SELECT * FROM paradas WHERE id_parada = :id")
        result = self.db.execute(query, {"id": stop_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_stop(self, id_ruta: int, id_estacion: int, orden: int):
        query = text("""
            INSERT INTO paradas (id_ruta, id_estacion, orden)
            VALUES (:id_ruta, :id_estacion, :orden)
        """)
        self.db.execute(query, {
            "id_ruta": id_ruta,
            "id_estacion": id_estacion,
            "orden": orden
        })
        self.db.commit()

    def update_stop(self, stop_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE paradas SET {set_clause} WHERE id_parada = :id")
        kwargs["id"] = stop_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_stop(self, stop_id: int):
        query = text("DELETE FROM paradas WHERE id_parada = :id")
        self.db.execute(query, {"id": stop_id})
        self.db.commit()

    def get_all_stops(self):
        query = text(
            "SELECT p.*, r.nombre AS ruta, e.nombre AS estacion "
            "FROM paradas p "
            "INNER JOIN rutas r ON p.id_ruta = r.id_ruta "
            "INNER JOIN estaciones e ON p.id_estacion = e.id_estacion"
        )
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]