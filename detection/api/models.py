from pydantic import BaseModel


class DetectionResult(BaseModel):
    date: str
    vehicle_type: str
    color: str
    number: str
    vehicle: list
    plate: list
