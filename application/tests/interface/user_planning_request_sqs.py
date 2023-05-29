import pytest
from unittest.mock import patch
from pydantic import BaseModel

from src.domain.entities.place import PlaceEntity
from src.interface.adapter.serverless.sqs import UserPlanningRequestSqsAdapter
from src.infrastructure.repositories.database.dynamo.place import PlaceDynamoDBRepository
from src.infrastructure.repositories.database.dynamo.request_logging import RequestLoggingDynamoDBRepository


class AwsContextClass(BaseModel):
    aws_request_id: str

@pytest.fixture
def mock_event_sqs_request():
    return {
        'Records': [
            {
                'messageId': '19dd0b57-b21e-4ac0-8d9a-7798dd73b3de',
                'body': '{"request_id": "1234567890", "user_id": "1234567890", "place": "Tokyo", "days": 3, "start_date": "2021-01-01T00:00:00.00Z"}',
            }
        ]
    }

@pytest.fixture
def mock_context_api_gateway_request():
    return AwsContextClass(aws_request_id='1234567890')


@patch.object(RequestLoggingDynamoDBRepository, 'update_request_suggestion_status')
@patch.object(RequestLoggingDynamoDBRepository, 'update_request_suggestion_complete')
@patch.object(PlaceDynamoDBRepository, 'update_or_create_place_by_slug')
def test_user_planning_request_sqs_adapter(
        mocker_place_repository_update_or_create_place_by_slug,
        mocker_db_logging_repository_update_request_complete,
        mocker_db_logging_repository_update_request_status, 
        mock_event_sqs_request, mock_context_api_gateway_request
    ):

    # mocker_place_repository_update_or_create_place_by_slug.return_value = PlaceEntity(
    #     place_slug='japan-tokyo',
    #     name='Tokyo Tower',
    #     place_id='1234567890',
    #     address='Tokyo, Japan',
    #     location_lat=35.658581,
    #     location_long=139.745433,
    #     country_name='Japan',
    #     provice='Tokyo',
    #     types=['tourist_attraction', 'point_of_interest', 'establishment'],
    #     description='Tokyo Tower is a communications and observation tower in the Shiba-koen district of Minato, Tokyo, Japan. It is 333.0 m tall, and was completed on 23 October 1958. It is the second-tallest structure in Japan, after the 634.0 m Tokyo Skytree, and the second-tallest self-supporting steel tower in the world, after the 350 m KVLY-TV mast in Blanchard, North Dakota, United States. The tower is an Eiffel Tower design, and one of the most recognizable structures in Japan. It is nicknamed "Tokyo Tower" or simply "Tower" (東京タワー, Tōkyō Tawā?).',
    # )
    UserPlanningRequestSqsAdapter(mock_event_sqs_request, mock_context_api_gateway_request).execute()

    # mocker_db_logging_repository_update_request_complete.assert_called_once()
