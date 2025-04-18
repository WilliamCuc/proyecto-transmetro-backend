from fastapi import APIRouter, HTTPException
from app.models.department import Department

router = APIRouter()
department_model = Department()

@router.get("/api/department/get-all")
def get_all_departments():
    return department_model.get_all_departments()

@router.get("/api/department/get/{department_id}")
def get_department(department_id: int):
    return department_model.get_by_id(department_id)
