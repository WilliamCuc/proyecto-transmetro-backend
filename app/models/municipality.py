from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Municipality:
    def get_by_id(self, municipality_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM municipios WHERE id_municipio = :id")
                result = db.execute(query, {"id": municipality_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener municipio por ID: {e}")
            return None

    def get_all_municipalities(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM municipios")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los municipios: {e}")
            return []

    def get_by_department(self, department_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM municipios WHERE id_departamento = :department_id")
                result = db.execute(query, {"department_id": department_id}).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener municipios por departamento: {e}")
            return []