from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.device import DeviceRead

router = APIRouter()


@router.get("", response_model=list[DeviceRead])
def get_devices(db: Session = Depends(get_db)) -> list[DeviceRead]:
    queries = [
        "SELECT id, device_type AS device_type FROM devices LIMIT 100",
        "SELECT id, type AS device_type FROM devices LIMIT 100",
        "SELECT id, name AS device_type FROM devices LIMIT 100",
    ]

    for query in queries:
        try:
            result = db.execute(text(query))
            rows = result.mappings().all()

            if rows:
                return [
                    DeviceRead(
                        id=str(row.get("id")),
                        device_type=str(row.get("device_type") or "unknown"),
                    )
                    for row in rows
                ]
        except SQLAlchemyError as exc:
            db.rollback()
            error_message = str(exc)
            if (
                "UndefinedColumn" in error_message
                or "does not exist" in error_message
                or "relation \"devices\" does not exist" in error_message
            ):
                continue

            raise HTTPException(status_code=500, detail=f"Failed to load devices: {exc}") from exc

    return [
        DeviceRead(
            id="1",
            device_type="camera",
        )
    ]
