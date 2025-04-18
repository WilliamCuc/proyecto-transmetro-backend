from sqlalchemy import text
from app.db.database import SessionLocal

class Department:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_id(self, department_id: int):
        query = text("SELECT * FROM departamentos WHERE id_departamento = :id")
        result = self.db.execute(query, {"id": department_id}).fetchone()
        return dict(result._mapping) if result else None

    def get_all_departments(self):
        query = text("SELECT * FROM departamentos")
        result = self.db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]