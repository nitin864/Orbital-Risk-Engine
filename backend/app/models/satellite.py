from pydantic import BaseModel


class Satellite(BaseModel):
    """
    Represents a single satellite's raw orbital data (TLE format).
    """
    name: str
    line1: str
    line2: str