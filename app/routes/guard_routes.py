from fastapi import APIRouter, HTTPException
from app.models.guard import Guard

router = APIRouter()
guard_model = Guard()

@router.get("/api/guard/get-all")
def get_all_guards():
    try:
        return guard_model.get_all_guards()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los guardias: {str(e)}")

@router.get("/api/guard/get/{guard_id}")
def get_guard(guard_id: int):
    try:
        guard = guard_model.get_by_id(guard_id)
        if not guard:
            raise HTTPException(status_code=404, detail="Guardia no encontrado")
        return guard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el guardia: {str(e)}")

@router.post("/api/guard/create")
def create_guard(nombre: str, id_acceso: int):
    try:
        guard_model.create_guard(nombre, id_acceso)
        return {"message": "Guardia creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el guardia: {str(e)}")

@router.put("/api/guard/update")
def update_guard(
    guard_id: int,
    nombre: str = None,
    id_acceso: int = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if id_acceso is not None:
            update_data['id_acceso'] = id_acceso
        
        guard_model.update_guard(guard_id, **update_data)
        return {"message": "Guardia actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el guardia: {str(e)}")

@router.delete("/api/guard/delete")
def delete_guard(guard_id: int):
    try:
        guard_model.delete_guard(guard_id)
        return {"message": "Guardia eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el guardia: {str(e)}")