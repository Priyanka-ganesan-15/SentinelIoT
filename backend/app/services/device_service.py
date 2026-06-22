from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceResponse
from app.services.simulator.device_generator import DeviceGenerator


class DeviceService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.generator = DeviceGenerator()

    def create_simulation(self, device_count: int) -> int:
        self._ensure_devices_schema()
        devices = self.generator.generate_devices(device_count)

        self.db.bulk_save_objects(devices)
        self.db.commit()
        return len(devices)

    def get_devices(self) -> list[DeviceResponse]:
        self._ensure_devices_schema()
        devices = self.db.query(Device).order_by(Device.created_at.desc()).all()
        return [
            DeviceResponse(
                id=str(device.id),
                name=device.name,
                device_type=device.device_type,
                state=device.state,
                cpu=float(device.cpu),
                memory=float(device.memory),
                battery=float(device.battery),
                trust_score=float(device.trust_score),
                created_at=device.created_at,
            )
            for device in devices
        ]

    def delete_simulation(self) -> int:
        self._ensure_devices_schema()
        deleted = self.db.query(Device).delete()
        self.db.commit()
        return int(deleted)

    def _ensure_devices_schema(self) -> None:
        statements = [
            """
            CREATE TABLE IF NOT EXISTS devices (
                id TEXT PRIMARY KEY,
                name TEXT,
                device_type TEXT,
                state TEXT,
                cpu DOUBLE PRECISION,
                memory DOUBLE PRECISION,
                battery DOUBLE PRECISION,
                trust_score DOUBLE PRECISION,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
            """,
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS name TEXT",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS device_type TEXT",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS state TEXT",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS cpu DOUBLE PRECISION",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS memory DOUBLE PRECISION",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS battery DOUBLE PRECISION",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS trust_score DOUBLE PRECISION",
            "ALTER TABLE devices ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW()",
        ]

        try:
            for stmt in statements:
                self.db.execute(text(stmt))
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
