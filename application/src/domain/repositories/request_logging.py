from abc import ABC, abstractmethod

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.domain.entities.ai.travel_guider import TravelGuiderEntity


class RequestLoggingRepository(ABC):
    
    @abstractmethod
    def save_request_suggestion_entity(self, user_request_planning: UserPlanningRequestEntity):
        pass

    @abstractmethod
    def update_request_suggestion_status(self, user_request_planning: UserPlanningRequestEntity, status: str):
        pass

    @abstractmethod
    def update_request_suggestion_complete(self, user_request_planning: UserPlanningRequestEntity, result: TravelGuiderEntity):
        pass

    @abstractmethod
    def update_request_suggestion_error(self, user_request_planning: UserPlanningRequestEntity, error: Exception):
        pass
