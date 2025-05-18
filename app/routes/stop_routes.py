from fastapi import APIRouter, HTTPException
from app.models.stop import Stop

router = APIRouter()
stop_model = Stop()

@router.get("/api/stop/get-all")
def get_all_stops():
    return stop_model.get_all_stops()

@router.get("/api/stop/get/{stop_id}")
def get_stop(stop_id: int):
    return stop_model.get_by_id(stop_id)

@router.post("/api/stop/create")
def create_stop(id_ruta: int, id_estacion: int, orden: int):
    stop_model.create_stop(id_ruta, id_estacion, orden)
    return {"message": "Parada creada exitosamente"}

@router.put("/api/stop/update")
def update_stop(
    stop_id: int,
    id_ruta: int = None,
    id_estacion: int = None,
    orden: int = None
):
    try:
        update_data = {}
        if id_ruta is not None:
            update_data['id_ruta'] = int(id_ruta)
        if id_estacion is not None:
            update_data['id_estacion'] = int(id_estacion)
        if orden is not None:
            update_data['orden'] = int(orden)
        
        stop_model.update_stop(stop_id, **update_data)
        return {"message": "Parada actualizada exitosamente"}
    except Exception as e:
        print(f"Error updating stop: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/stop/delete")
def delete_stop(stop_id: int):
    stop_model.delete_stop(stop_id)
    return {"message": "Parada eliminada exitosamente"}