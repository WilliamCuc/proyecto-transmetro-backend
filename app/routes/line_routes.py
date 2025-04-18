from fastapi import APIRouter, HTTPException
from app.models.line import Line

router = APIRouter()
line_model = Line()

@router.get("/api/line/get-all")
def get_all_lines():
    return line_model.get_all_lines()

@router.get("/api/line/get/{line_id}")
def get_line(line_id: int):
    return line_model.get_by_id(line_id)

@router.post("/api/line/create")
def create_line(nombre: str, distancia_total: float, estado: int):
    line_model.create_line(nombre, distancia_total, estado)
    return {"message": "Línea creada exitosamente"}

@router.put("/api/line/update")
def update_line(
    line_id: int,
    nombre: str = None,
    distancia_total: float = None,
    estado: int = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if distancia_total is not None:
            update_data['distancia_total'] = float(distancia_total)
        if estado is not None:
            update_data['estado'] = int(estado)
        
        line_model.update_line(line_id, **update_data)
        return {"message": "Línea actualizada exitosamente"}
    except Exception as e:
        print(f"Error updating line: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/line/delete")
def delete_line(line_id: int):
    line_model.delete_line(line_id)
    return {"message": "Línea eliminada exitosamente"}