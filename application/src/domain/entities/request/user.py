from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from src.domain.entities.ai.travel_guider import TravelGuiderEntity


class UserPlanningRequestEntity(BaseModel):
    request_id: str
    user_id: str
    place: str
    days: int
    start_date: Optional[datetime]


class UserPlanningResponseAcceptRequestEntity(BaseModel):
    user_id: str
    request_id: str
    status: str


class UserPlanningSuggestionResponseEntity(BaseModel):
    user_id: str
    requested_place: str
    requested_start_date: Optional[datetime]
    request_id: str
    status: str
    timestamp: int
    requested_timestamp: int
    requested_days: int
    result: Optional[TravelGuiderEntity]
    