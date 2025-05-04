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
def create_user(
    nombre: str,
    apellido: str,
    correo: str,
    contrasena: str,
    rol: str,
    estado: str
):
    try:
        user_model = User()
        user_model.create_user(
            nombre,
            apellido,
            correo,
            contrasena,
            rol,
            int(estado)
        )
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/user/update")
def update_user(
    user_id: int,
    nombre: str = None,
    apellido: str = None,
    correo: str = None,
    rol: str = None,
    estado: str = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if apellido is not None:
            update_data['apellido'] = apellido
        if correo is not None:
            update_data['correo'] = correo
        if rol is not None:
            update_data['rol'] = int(rol)
        if estado is not None:
            update_data['estado'] = int(estado)
        
        user_model = User()
        user_model.update_user(user_id, **update_data)
        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/user/delete")
def delete_user(user_id: int):
    user_model.delete_user(user_id)
    return {"message": "User deleted successfully"}

@router.get("/api/user/get-all")
async def get_all_users():
    try:
        user_model = User()
        users = user_model.get_all_users()
        return users
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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