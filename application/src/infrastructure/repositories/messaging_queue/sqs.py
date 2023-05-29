import boto3
import json

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.domain.repositories.messaging_queue import MessagingQueueRepository
from src.shared.convert import datetime_to_str_iso_datetime
from src.settings import SQS_URL_BUDDYGUIDER_REQUEST_SUGGESTION


class SqsRepository(MessagingQueueRepository):
    def __init__(self, queue_url: str) -> None:
        self.sqs_client = boto3.client('sqs')
        self.sqs_url = queue_url

    def publish(self, message: dict):
        message_body = self.__convert_to_sqs_message(message)
        self.sqs_client.send_message(
            QueueUrl=self.sqs_url,
            MessageBody=message_body
        )

    def __convert_to_sqs_message(self, message: dict):
        return json.dumps(message)


class SqsRequestSuggestionsRepository(SqsRepository):

    def __init__(self) -> None:
        super().__init__(queue_url=SQS_URL_BUDDYGUIDER_REQUEST_SUGGESTION)

    def publish(self, user_planning_request: UserPlanningRequestEntity):
        start_date = datetime_to_str_iso_datetime(user_planning_request.start_date)
        message = {
            'user_id': user_planning_request.user_id,
            'request_id': user_planning_request.request_id,
            'place': user_planning_request.place,
            'days': user_planning_request.days,
            'start_date': start_date
        }
        return super().publish(message)
