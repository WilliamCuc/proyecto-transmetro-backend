from fastapi import APIRouter, HTTPException
from app.models.ticket import Ticket

router = APIRouter()
ticket_model = Ticket()

@router.get("/api/ticket/get-all")
def get_all_tickets():
    try:
        return ticket_model.get_all_tickets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los boletos: {str(e)}")

@router.get("/api/ticket/get/{ticket_id}")
def get_ticket(ticket_id: int):
    try:
        ticket = ticket_model.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Boleto no encontrado")
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el boleto: {str(e)}")

@router.post("/api/ticket/create")
def create_ticket(id_usuario: int, id_ruta: int, fecha_compra: str, precio: float):
    try:
        ticket_model.create_ticket(id_usuario, id_ruta, fecha_compra, precio)
        return {"message": "Boleto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el boleto: {str(e)}")

@router.put("/api/ticket/update")
def update_ticket(
    ticket_id: int,
    id_usuario: int = None,
    id_ruta: int = None,
    fecha_compra: str = None,
    precio: float = None
):
    try:
        update_data = {}
        if id_usuario is not None:
            update_data['id_usuario'] = id_usuario
        if id_ruta is not None:
            update_data['id_ruta'] = id_ruta
        if fecha_compra is not None:
            update_data['fecha_compra'] = fecha_compra
        if precio is not None:
            update_data['precio'] = precio
        
        ticket_model.update_ticket(ticket_id, **update_data)
        return {"message": "Boleto actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el boleto: {str(e)}")

@router.delete("/api/ticket/delete")
def delete_ticket(ticket_id: int):
    try:
        ticket_model.delete_ticket(ticket_id)
        return {"message": "Boleto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el boleto: {str(e)}")