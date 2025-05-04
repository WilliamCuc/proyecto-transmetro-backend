from fastapi import APIRouter, HTTPException
from app.models.schedule import Schedule as ScheduleModel

router = APIRouter()
schedule_model = ScheduleModel()

@router.get("/api/schedule/get-all")
def get_all_schedules():
    try:
        return schedule_model.get_all_schedules()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los horarios: {str(e)}")

@router.get("/api/schedule/get/{schedule_id}")
def get_schedule(schedule_id: int):
    try:
        schedule = schedule_model.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        return schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el horario: {str(e)}")

@router.post("/api/schedule/create")
def create_schedule(id_ruta: int, hora_salida: str, hora_llegada: str):
    try:
        schedule_model.create_schedule(id_ruta, hora_salida, hora_llegada)
        return {"message": "Horario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el horario: {str(e)}")

@router.put("/api/schedule/update")
def update_schedule(
    schedule_id: int,
    id_ruta: int = None,
    hora_salida: str = None,
    hora_llegada: str = None
):
    try:
        update_data = {}
        if id_ruta is not None:
            update_data['id_ruta'] = id_ruta
        if hora_salida is not None:
            update_data['hora_salida'] = hora_salida
        if hora_llegada is not None:
            update_data['hora_llegada'] = hora_llegada
        
        schedule_model.update_schedule(schedule_id, **update_data)
        return {"message": "Horario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el horario: {str(e)}")

@router.delete("/api/schedule/delete")
def delete_schedule(schedule_id: int):
    try:
        schedule_model.delete_schedule(schedule_id)
        return {"message": "Horario eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el horario: {str(e)}")