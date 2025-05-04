from fastapi import APIRouter, HTTPException
from app.models.pilot import Pilot

router = APIRouter()
pilot_model = Pilot()

@router.get("/api/pilot/get-all")
def get_all_pilots():
    try:
        return pilot_model.get_all_pilots()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los pilotos: {str(e)}")

@router.get("/api/pilot/get/{pilot_id}")
def get_pilot(pilot_id: int):
    try:
        pilot = pilot_model.get_by_id(pilot_id)
        if not pilot:
            raise HTTPException(status_code=404, detail="Piloto no encontrado")
        return pilot
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el piloto: {str(e)}")

@router.post("/api/pilot/create")
def create_pilot(nombre: str, historial_educativo: str, direccion: str, telefono: str, id_bus: int):
    try:
        pilot_model.create_pilot(nombre, historial_educativo, direccion, telefono, id_bus)
        return {"message": "Piloto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el piloto: {str(e)}")

@router.put("/api/pilot/update")
def update_pilot(
    pilot_id: int,
    nombre: str = None,
    historial_educativo: str = None,
    direccion: str = None,
    telefono: str = None,
    id_bus: int = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if historial_educativo is not None:
            update_data['historial_educativo'] = historial_educativo
        if direccion is not None:
            update_data['direccion'] = direccion
        if telefono is not None:
            update_data['telefono'] = telefono
        if id_bus is not None:
            update_data['id_bus'] = id_bus
        
        pilot_model.update_pilot(pilot_id, **update_data)
        return {"message": "Piloto actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el piloto: {str(e)}")

@router.delete("/api/pilot/delete")
def delete_pilot(pilot_id: int):
    try:
        pilot_model.delete_pilot(pilot_id)
        return {"message": "Piloto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el piloto: {str(e)}")