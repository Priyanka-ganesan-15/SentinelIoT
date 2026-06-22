from datetime import datetime

from pydantic import BaseModel


class DeviceResponse(BaseModel):
    id: str
    name: str
    device_type: str
    state: str
    cpu: float
    memory: float
    battery: float
    trust_score: float
    created_at: datetime

    model_config = {"from_attributes": True}


class SimulationCreateRequest(BaseModel):
    device_count: int = 1000
