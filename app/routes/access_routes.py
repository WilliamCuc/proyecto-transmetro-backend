from fastapi import APIRouter, HTTPException
from app.models.access import Access

router = APIRouter()
access_model = Access()

@router.get("/api/access/get-all")
def get_all_accesses():
    try:
        return access_model.get_all_accesses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los accesos: {str(e)}")

@router.get("/api/access/get/{access_id}")
def get_access(access_id: int):
    try:
        access = access_model.get_by_id(access_id)
        if not access:
            raise HTTPException(status_code=404, detail="Acceso no encontrado")
        return access
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el acceso: {str(e)}")

@router.post("/api/access/create")
def create_access(descripcion: str, id_estacion: int):
    try:
        access_model.create_access(descripcion, id_estacion)
        return {"message": "Acceso creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el acceso: {str(e)}")

@router.put("/api/access/update")
def update_access(
    access_id: int,
    descripcion: str = None,
    id_estacion: int = None
):
    try:
        update_data = {}
        if descripcion is not None:
            update_data['descripcion'] = descripcion
        if id_estacion is not None:
            update_data['id_estacion'] = id_estacion
        
        access_model.update_access(access_id, **update_data)
        return {"message": "Acceso actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el acceso: {str(e)}")

@router.delete("/api/access/delete")
def delete_access(access_id: int):
    try:
        access_model.delete_access(access_id)
        return {"message": "Acceso eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el acceso: {str(e)}")