from pydantic import BaseModel


class DeviceRead(BaseModel):
    id: str
    name: str | None = None
    device_type: str | None = None
    state: str | None = None
    cpu: float | None = None
    memory: float | None = None
    battery: float | None = None
    trust_score: float | None = None

    model_config = {"from_attributes": True}
