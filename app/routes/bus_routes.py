from fastapi import APIRouter, HTTPException
from app.models.bus import Bus

router = APIRouter()
bus_model = Bus()

@router.get("/api/bus/get-all")
def get_all_buses():
    try:
        return bus_model.get_all_buses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los buses: {str(e)}")

@router.get("/api/bus/get/{bus_id}")
def get_bus(bus_id: int):
    try:
        bus = bus_model.get_by_id(bus_id)
        if not bus:
            raise HTTPException(status_code=404, detail="Bus no encontrado")
        return bus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el bus: {str(e)}")

@router.post("/api/bus/create")
def create_bus(numero_bus: str, capacidad: int, estado: str, id_parqueo: int):
    try:
        bus_model.create_bus(numero_bus, capacidad, estado, id_parqueo)
        return {"message": "Bus creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el bus: {str(e)}")

@router.put("/api/bus/update")
def update_bus(
    bus_id: int,
    numero_bus: str = None,
    capacidad: int = None,
    estado: str = None,
    id_parqueo: int = None
):
    try:
        update_data = {}
        if numero_bus is not None:
            update_data['numero_bus'] = numero_bus
        if capacidad is not None:
            update_data['capacidad'] = capacidad
        if estado is not None:
            update_data['estado'] = estado
        if id_parqueo is not None:
            update_data['id_parqueo'] = id_parqueo
        
        bus_model.update_bus(bus_id, **update_data)
        return {"message": "Bus actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el bus: {str(e)}")

@router.delete("/api/bus/delete")
def delete_bus(bus_id: int):
    try:
        bus_model.delete_bus(bus_id)
        return {"message": "Bus eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el bus: {str(e)}")