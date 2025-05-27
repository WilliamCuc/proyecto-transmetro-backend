from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Report:
    def get_guard_by_station(self, id_estacion=None):
        try:
            with SessionLocal() as db:
                base_query = """
                    SELECT  ROW_NUMBER() OVER () AS id_registro,
                            b.nombre AS estacion,
                            a.descripcion AS acceso,
                            c.nombre AS guardia
                    FROM accesos a
                    LEFT JOIN estaciones b ON b.id_estacion = a.id_estacion
                    LEFT JOIN guardias c ON c.id_acceso = a.id_acceso
                """
                params = {}
                if id_estacion:
                    base_query += " WHERE b.id_estacion = :id_estacion"
                    params["id_estacion"] = id_estacion
                query = text(base_query)
                result = db.execute(query, params).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener guardias por estación: {e}")
            return []

    def get_sold_ticket(self, fecha_inicio=None, fecha_fin=None):
        try:
            with SessionLocal() as db:
                base_query = """
                    SELECT  a.id_boleto AS numero_boleto,
                            CONCAT(b.nombre, ' ', b.apellido) AS usuario,
                            b.correo,
                            a.fecha_compra,
                            c.nombre AS ruta,
                            a.precio
                    FROM boletos a
                    INNER JOIN usuarios b ON a.id_usuario = b.id_usuario
                    INNER JOIN rutas c ON a.id_ruta = c.id_ruta
                """
                params = {}
                if fecha_inicio and fecha_fin:
                    base_query += " WHERE a.fecha_compra BETWEEN :fecha_inicio AND :fecha_fin"
                    params["fecha_inicio"] = fecha_inicio + " 00:00:00"
                    params["fecha_fin"] = fecha_fin + " 23:59:59"
                query = text(base_query)
                result = db.execute(query, params).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener boletos vendidos: {e}")
            return []