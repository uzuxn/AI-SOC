from pydantic import BaseModel
from typing import Dict

class LogInput(BaseModel):
    source_ip: str
    event_type: str
    message: str
    features: Dict[str, float]