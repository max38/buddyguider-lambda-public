from abc import ABC, abstractmethod

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.domain.entities.ai.travel_guider import TravelGuiderEntity


class AiRepository(ABC):

    @abstractmethod
    def travel_planning_suggestion(self, user_planning_request: UserPlanningRequestEntity) -> TravelGuiderEntity:
        pass
