from pydantic import BaseModel, validator
from typing import List, Dict, Optional


class PlaceOpenPeriodEntity(BaseModel):
    open_day: int
    open_time: str
    close_day: int
    close_time: str
    timezone: str


class PlaceEntity(BaseModel):
    place_slug: str
    place_id: str
    name: str
    address: str
    location_lat: float
    location_long: float
    country_name: str
    province: str
    rating: float = 0
    open_periods: List[PlaceOpenPeriodEntity] = []
    types: List[str] = []
    trip_types: List[str] = []
    # place_price_level: int
    phone_number: Optional[str] = ''
    email: Optional[str] = ''
    website: Optional[str] = ''
    description: str
    photos: List[str] = []
