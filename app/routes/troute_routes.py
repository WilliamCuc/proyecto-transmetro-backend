from fastapi import APIRouter, HTTPException
from app.models.troute import Route as RouteModel

router = APIRouter()
route_model = RouteModel()

@router.get("/api/route/get-all")
def get_all_routes():
    try:
        return route_model.get_all_routes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las rutas: {str(e)}")

@router.get("/api/route/get/{route_id}")
def get_route(route_id: int):
    try:
        route = route_model.get_by_id(route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return route
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la ruta: {str(e)}")

@router.post("/api/route/create")
def create_route(nombre: str, descripcion: str, id_linea: int):
    try:
        route_model.create_route(nombre, descripcion, id_linea)
        return {"message": "Ruta creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la ruta: {str(e)}")

@router.put("/api/route/update")
def update_route(
    route_id: int,
    nombre: str = None,
    descripcion: str = None,
    id_linea: int = None
):
    try:
        update_data = {}
        if nombre is not None:
            update_data['nombre'] = nombre
        if descripcion is not None:
            update_data['descripcion'] = descripcion
        if id_linea is not None:
            update_data['id_linea'] = id_linea
        
        route_model.update_route(route_id, **update_data)
        return {"message": "Ruta actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la ruta: {str(e)}")

@router.delete("/api/route/delete")
def delete_route(route_id: int):
    try:
        route_model.delete_route(route_id)
        return {"message": "Ruta eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la ruta: {str(e)}")