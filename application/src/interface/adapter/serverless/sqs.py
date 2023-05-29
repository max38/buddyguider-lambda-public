import json 

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.use_cases.get_plan_suggession import GetPlanSuggestionUseCase
from src.interface.adapter.serverless import ServerLessAdapter
from src.infrastructure.repositories.chatgpt.ai_guider import ChatGPTGuiderRepository
from src.infrastructure.repositories.database.dynamo.place import PlaceDynamoDBRepository
from src.infrastructure.repositories.database.dynamo.request_logging import RequestLoggingDynamoDBRepository

from src.shared.convert import str_iso_datetime_to_datetime


class SqsAdapter(ServerLessAdapter):

    def __init__(self, event, context) -> None:
        self.event = event
        self.context = context
        self.records = self._get_records_from_event()

    def _get_records_from_event(self):
        return self.event['Records']
    
    def _get_body_data_from_event(self):
        pass
        
    def _get_body_data_from_record(self, record):
        return json.loads(record['body'])

    def execute(self):
        return self.__response(200, self._get_body_data_from_event()) 


class UserPlanningRequestSqsAdapter(SqsAdapter):

    def execute(self):
        for record in self.records:
            self._execute_body_record(self._get_body_data_from_record(record))
    
    def _execute_body_record(self, message_body):
        start_date = str_iso_datetime_to_datetime(message_body['start_date']) if 'start_date' in message_body else None
        
        user_planning_request = UserPlanningRequestEntity(
            request_id=message_body['request_id'],
            user_id=message_body['user_id'],
            place=message_body['place'],
            days=message_body['days'],
            start_date=start_date,
        )
        GetPlanSuggestionUseCase(
            ai_guider_repository=ChatGPTGuiderRepository(),
            db_logging_repository=RequestLoggingDynamoDBRepository(),
            place_repository=PlaceDynamoDBRepository(),
        ).execute(user_planning_request)
    
    # def response(self, status_code: int, body_data: dict):
    #     body = json.dumps(body_data)
    #     return {
    #         'statusCode': status_code,
    #         "headers": {
    #             "Content-Type": "application/json"
    #         },
    #         'body': body
    #     }
