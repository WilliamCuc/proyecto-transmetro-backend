from fastapi import APIRouter, HTTPException
from app.models.municipality import Municipality

router = APIRouter()
municipality_model = Municipality()

@router.get("/api/municipality/get-all")
def get_all_municipalities():
    return municipality_model.get_all_municipalities()

@router.get("/api/municipality/get/{municipality_id}")
def get_municipality(municipality_id: int):
    return municipality_model.get_by_id(municipality_id)

@router.get("/api/municipality/by-department/{department_id}")
def get_municipalities_by_department(department_id: int):
    return municipality_model.get_by_department(department_id)
