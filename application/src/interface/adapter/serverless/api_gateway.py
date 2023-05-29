import uuid

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.interface.adapter.serverless import ServerLessAdapter
from src.infrastructure.repositories.messaging_queue.sqs import SqsRequestSuggestionsRepository
from src.infrastructure.repositories.database.dynamo.request_logging import RequestLoggingDynamoDBRepository
from src.infrastructure.repositories.database.dynamo.place import PlaceDynamoDBRepository
from src.use_cases.get_plan_suggession import GetPlanSuggestionAcceptUseCase

from src.shared.convert import str_iso_datetime_to_datetime, dict_to_json
from src.shared.encryption import encrypt


class ApiGatwayAdapter(ServerLessAdapter):

    def execute(self):
        return self.__response(200, self._get_body_data_from_event())
    
    def response(self, status_code: int, body_data: dict):
        body = dict_to_json(body_data)
        return {
            'statusCode': status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*", # Allow from anywhere 
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH", #  Allow only GET request 
            },
            'body': body
        }


class UserPlanningRequestApiAdapter(ApiGatwayAdapter):
    def execute(self):
        start_date = str_iso_datetime_to_datetime(self.body['start_date']) if 'start_date' in self.body else None

        user_planning_request = UserPlanningRequestEntity(
            request_id=self._get_request_id_from_context(),
            user_id=str(uuid.uuid4()),
            place=self.body['place'],
            days=self.body['days'],
            start_date=start_date
        )

        response = GetPlanSuggestionAcceptUseCase(
            queue_repository=SqsRequestSuggestionsRepository(),
            db_logging_repository=RequestLoggingDynamoDBRepository()
        ).execute(user_planning_request)

        return self.response(200, response.dict())


class GetSuggestionResultApiAdapter(ApiGatwayAdapter):
    def execute(self):
        place_repository = PlaceDynamoDBRepository()
        db_logging_repository = RequestLoggingDynamoDBRepository(place_repository)
        request_id = self._get_request_id_from_path_parameter()
        response = db_logging_repository.get_suggestion_request(request_id)

        # response_data = {
        #     'data': encrypt(dict_to_json(response.dict())),
        #     'data2': encrypt("test")
        # }

        # return self.response(200, response_data)
        return self.response(200, response.dict())
    
    def _get_request_id_from_path_parameter(self):
        return self.event['pathParameters']['request_id']


class GetPlaceInformationApiAdapter(ApiGatwayAdapter):
    def execute(self):
        place_slug = self._get_place_slug_from_path_parameter()
        db_place_repository = PlaceDynamoDBRepository()
        response = db_place_repository.get_place_by_slug(place_slug)
        if response is None:
            return self.response(404, {'message': 'Place not found'})
        return self.response(200, response.dict())

    def _get_place_slug_from_path_parameter(self):
        return self.event['pathParameters']['place_slug']
