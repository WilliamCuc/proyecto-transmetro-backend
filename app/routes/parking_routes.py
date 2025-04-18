from fastapi import APIRouter, HTTPException
from app.models.parking import Parking

router = APIRouter()
parking_model = Parking()

@router.get("/api/parking/get-all")
def get_all_parkings():
    try:
        return parking_model.get_all_parkings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los parqueos: {str(e)}")

@router.get("/api/parking/get/{parking_id}")
def get_parking(parking_id: int):
    try:
        parking = parking_model.get_by_id(parking_id)
        if not parking:
            raise HTTPException(status_code=404, detail="Parqueo no encontrado")
        return parking
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el parqueo: {str(e)}")

@router.post("/api/parking/create")
def create_parking(id_estacion: int, codigo: str):
    try:
        parking_model.create_parking(id_estacion, codigo)
        return {"message": "Parqueo creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el parqueo: {str(e)}")

@router.put("/api/parking/update")
def update_parking(
    parking_id: int,
    id_estacion: int = None,
    codigo: str = None
):
    try:
        update_data = {}
        if id_estacion is not None:
            update_data['id_estacion'] = id_estacion
        if codigo is not None:
            update_data['codigo'] = codigo
        
        parking_model.update_parking(parking_id, **update_data)
        return {"message": "Parqueo actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el parqueo: {str(e)}")

@router.delete("/api/parking/delete")
def delete_parking(parking_id: int):
    try:
        parking_model.delete_parking(parking_id)
        return {"message": "Parqueo eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el parqueo: {str(e)}")