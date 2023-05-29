from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from src.domain.entities.place import PlaceEntity


class PlaceGuiderActivityEntity(PlaceEntity):
    place_id: Optional[str]
    address: Optional[str]
    suggest_time_spend: str
    activity: str


class DailyDetailGuiderEntity(BaseModel):
    activites: List[PlaceGuiderActivityEntity]
    description: str
    day: int


class TravelGuiderEntity(BaseModel):
    request_id: str
    user_id: str
    place: str
    days: int
    start_date: Optional[datetime]
    message: dict
    daily_suggests: Dict[str, DailyDetailGuiderEntity]



