import traceback

from src.domain.entities.request.user import UserPlanningRequestEntity, UserPlanningResponseAcceptRequestEntity
from src.domain.repositories.ai_guider import AiRepository
from src.domain.repositories.messaging_queue import MessagingQueueRepository
from src.domain.repositories.request_logging import RequestLoggingRepository
from src.domain.repositories.place import PlaceRepository

# from src.shared.convert import dict_to_json

class GetPlanSuggestionUseCase:

    def __init__(self, ai_guider_repository: AiRepository, db_logging_repository: RequestLoggingRepository, place_repository: PlaceRepository) -> None:
        self.ai_guider_repository = ai_guider_repository
        self.db_logging_repository = db_logging_repository  
        self.place_repository = place_repository   

    def execute(self, user_planning_request: UserPlanningRequestEntity):
        try:
            self.db_logging_repository.update_request_suggestion_status(user_planning_request, 'PROCESSING')
            travel_guider = self.ai_guider_repository.travel_planning_suggestion(
                user_planning_request, place_repository=self.place_repository
            )
            self.db_logging_repository.update_request_suggestion_complete(user_planning_request, travel_guider)
        except Exception as e:
            self.db_logging_repository.update_request_suggestion_error(user_planning_request, traceback.format_exc())


class GetPlanSuggestionAcceptUseCase:

    def __init__(self, queue_repository: MessagingQueueRepository, db_logging_repository: RequestLoggingRepository) -> None:
        self.queue_repository = queue_repository  
        self.db_logging_repository = db_logging_repository  

    def execute(self, user_planning_request: UserPlanningRequestEntity) -> UserPlanningResponseAcceptRequestEntity:
        status = 'ACCEPTED'
        self.db_logging_repository.save_request_suggestion_entity(user_planning_request, status)
        self.queue_repository.publish(user_planning_request)
        request_response = UserPlanningResponseAcceptRequestEntity(
            user_id=user_planning_request.user_id,
            request_id=user_planning_request.request_id,
            status=status
        )
        return request_response
