import os
from fastapi import FastAPI
from app.middleware.cors_middleware import add_cors_middleware
from app.routes.user_routes import router as user_router
from app.routes.line_routes import router as line_router
from app.routes.municipality_routes import router as municipality_router
from app.routes.department_routes import router as department_router
from app.routes.station_routes import router as station_router
from app.routes.parking_routes import router as parking_router
from app.routes.troute_routes import router as troute_router
from app.routes.bus_routes import router as bus_router
from app.routes.pilot_routes import router as pilot_router
from app.routes.schedule_routes import router as schedule_router
from app.routes.guard_routes import router as guard_router
from app.routes.access_routes import router as access_router
from app.routes.stop_routes import router as stop_router
from app.routes.ticket_routes import router as ticket_router
from app.routes.report_routes import router as report_router
from app.config import settings

app = FastAPI()

add_cors_middleware(app)

app.include_router(user_router)
app.include_router(line_router)
app.include_router(municipality_router)
app.include_router(department_router)
app.include_router(station_router)
app.include_router(parking_router)
app.include_router(troute_router)
app.include_router(bus_router)
app.include_router(pilot_router)
app.include_router(schedule_router)
app.include_router(guard_router)
app.include_router(access_router)
app.include_router(stop_router)
app.include_router(ticket_router)
app.include_router(report_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)