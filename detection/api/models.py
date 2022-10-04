from pydantic import BaseModel


class DetectionResult(BaseModel):
    camera_id: int
    date: str
    color: str
    number: str
