from sqlalchemy import Column, Float, String

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