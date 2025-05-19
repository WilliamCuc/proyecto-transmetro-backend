from fastapi import APIRouter, HTTPException, Query
from app.models.report import Report

router = APIRouter()
report_model = Report()

@router.get("/api/report/guard-by-station")
def get_guard_by_station(id_estacion: int = Query(None)):
    try:
        return report_model.get_guard_by_station(id_estacion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el reporte: {str(e)}")
    
@router.get("/api/report/get-sold-ticket")
def get_sold_ticket(
    fecha_inicio: str = Query(None),
    fecha_fin: str = Query(None)
):
    try:
        return report_model.get_sold_ticket(fecha_inicio, fecha_fin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el reporte de boletos vendidos: {str(e)}")