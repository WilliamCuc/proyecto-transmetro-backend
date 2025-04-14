from fastapi import APIRouter, Request, HTTPException
from app.models.user import User
from app.db.database import get_db

router = APIRouter()
user_model = User()

@router.get("/api/user/get-by-id")
def get_user_by_id(user_id: int):
    user = user_model.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/api/user/create")
def create_user(nombre: str, apellido: str, correo: str, contrasena: str, rol: str, estado: bool):
    user_model.create_user(nombre, apellido, correo, contrasena, rol, estado)
    return {"message": "User created successfully"}

@router.put("/api/user/update")
def update_user(user_id: int, user_data: dict):
    user_model.update_user(user_id, **user_data)
    return {"message": "User updated successfully"}

@router.delete("/api/user/delete")
def delete_user(user_id: int):
    user_model.delete_user(user_id)
    return {"message": "User deleted successfully"}

@router.get("/api/user/get-all")
def get_all_users():
    users = user_model.get_all()
    return users

@router.post("/api/user/login")
async def login(request: Request):
    body = await request.json()
    correo = body.get("correo")
    contrasena = body.get("contrasena")

    if not correo or not contrasena:
        raise HTTPException(status_code=400, detail="Correo y contraseña son requeridos")

    user = user_model.login(correo, contrasena)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return user