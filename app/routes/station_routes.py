from fastapi import APIRouter, HTTPException
from app.models.station import Station

router = APIRouter()
station_model = Station()

@router.get("/api/station/get-all")
def get_all_stations():
    return station_model.get_all_stations()

@router.get("/api/station/get/{station_id}")
def get_station(station_id: int):
    return station_model.get_by_id(station_id)

@router.post("/api/station/create")
def create_station(nombre: str, ubicacion: str, id_municipio: int, id_linea: int):
    station_model.create_station(nombre, ubicacion, id_municipio, id_linea)
    return {"message": "Estación creada exitosamente"}

@router.put("/api/station/update")
def update_station(
    station_id: int,
    nombre: str = None,
    ubicacion: str = None,
    id_municipio: int = None,
    id_linea: int = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if ubicacion is not None:
            update_data['ubicacion'] = ubicacion
        if id_municipio is not None:
            update_data['id_municipio'] = int(id_municipio)
        if id_linea is not None:
            update_data['id_linea'] = int(id_linea)
        
        station_model.update_station(station_id, **update_data)
        return {"message": "Estación actualizada exitosamente"}
    except Exception as e:
        print(f"Error updating station: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/line/delete")
def delete_station(station_id: int):
    station_model.delete_station(station_id)
    return {"message": "Estación eliminada exitosamente"}