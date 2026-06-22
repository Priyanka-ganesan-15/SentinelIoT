from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.device import DeviceResponse, SimulationCreateRequest
from app.services.device_service import DeviceService

router = APIRouter()


@router.get("/devices", response_model=list[DeviceResponse])
def get_devices(db: Session = Depends(get_db)) -> list[DeviceResponse]:
    service = DeviceService(db)
    try:
        return service.get_devices()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load devices: {exc}") from exc


@router.post("/simulation/create")
def create_simulation(payload: SimulationCreateRequest, db: Session = Depends(get_db)) -> dict[str, int | str]:
    if payload.device_count < 1:
        raise HTTPException(status_code=400, detail="device_count must be greater than 0")

    service = DeviceService(db)
    try:
        created_count = service.create_simulation(payload.device_count)
        return {"message": "Simulation created", "devices_created": created_count}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create simulation: {exc}") from exc


@router.delete("/simulation")
def delete_simulation(db: Session = Depends(get_db)) -> dict[str, int | str]:
    service = DeviceService(db)
    try:
        deleted_count = service.delete_simulation()
        return {"message": "Simulation deleted", "devices_deleted": deleted_count}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail=f"Failed to delete simulation: {exc}") from exc
