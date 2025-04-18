from sqlalchemy import text
from app.db.database import SessionLocal

class Station:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, station_id: int):
        query = text("SELECT * FROM estaciones WHERE id_estacion = :id")
        result = self.db.execute(query, {"id": station_id}).fetchone()
        return dict(result._mapping) if result else None

    def create_station(self, nombre: str, ubicacion: str, id_municipio: int):
        query = text("""
            INSERT INTO estaciones (nombre, ubicacion, id_municipio)
            VALUES (:nombre, :ubicacion, :id_municipio)
        """)
        self.db.execute(query, {
            "nombre": nombre,
            "ubicacion": ubicacion,
            "id_municipio": id_municipio
        })
        self.db.commit()

    def update_station(self, station_id: int, **kwargs):
        set_clause = ", ".join([f"{key} = :{key}" for key in kwargs.keys()])
        query = text(f"UPDATE estaciones SET {set_clause} WHERE id_estacion = :id")
        kwargs["id"] = station_id
        self.db.execute(query, kwargs)
        self.db.commit()

    def delete_station(self, station_id: int):
        query = text("UPDATE estaciones SET estado = 0 WHERE id_estacion = :id")
        self.db.execute(query, {"id": station_id})
        self.db.commit()

    def get_all_stations(self):
        query = text("  SELECT a.*, b.nombre AS municipio, c.id_departamento, c.nombre AS departamento FROM estaciones a " \
        "               INNER JOIN municipios b ON a.id_municipio = b.id_municipio " \
        "               INNER JOIN departamentos c ON b.id_departamento = c.id_departamento ")    
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]