from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.db.database import get_db

router = APIRouter()
user_model = User()

@router.get("/user/get-by-id")
def get_user_by_id(user_id: int):
    user = user_model.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user/create")
def create_user(nombre: str, apellido: str, correo: str, contrasena: str, rol: str, estado: bool):
    user_model.create_user(nombre, apellido, correo, contrasena, rol, estado)
    return {"message": "User created successfully"}

@router.put("/user/update")
def update_user(user_id: int, user_data: dict):
    user_model.update_user(user_id, **user_data)
    return {"message": "User updated successfully"}

@router.delete("/user/delete")
def delete_user(user_id: int):
    user_model.delete_user(user_id)
    return {"message": "User deleted successfully"}