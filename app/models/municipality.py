from sqlalchemy import text
from app.db.database import SessionLocal

class Municipality:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, municipality_id: int):
        query = text("SELECT * FROM municipios WHERE id_municipio = :id")
        result = self.db.execute(query, {"id": municipality_id}).fetchone()
        return dict(result._mapping) if result else None

    def get_all_municipalities(self):
        query = text("SELECT * FROM municipios")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    
    def get_by_department(self, department_id: int):
        query = text("SELECT * FROM municipios WHERE id_departamento = :department_id")
        result = self.db.execute(query, {"department_id": department_id}).fetchall()
        return [dict(row._mapping) for row in result]