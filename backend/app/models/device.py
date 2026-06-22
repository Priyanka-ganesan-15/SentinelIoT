from sqlalchemy import Column, DateTime, Float, String, func

from app.db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True)
    name = Column(String)
    device_type = Column(String)
    state = Column(String)
    cpu = Column(Float)
    memory = Column(Float)
    battery = Column(Float)
    trust_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)