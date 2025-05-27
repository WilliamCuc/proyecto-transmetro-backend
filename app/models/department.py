from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import SessionLocal

class Department:
    def get_by_id(self, department_id: int):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM departamentos WHERE id_departamento = :id")
                result = db.execute(query, {"id": department_id}).fetchone()
                return dict(result._mapping) if result else None
        except SQLAlchemyError as e:
            print(f"Error al obtener departamento por ID: {e}")
            return None

    def get_all_departments(self):
        try:
            with SessionLocal() as db:
                query = text("SELECT * FROM departamentos")
                result = db.execute(query).fetchall()
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los departamentos: {e}")
            return []