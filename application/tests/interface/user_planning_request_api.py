import pytest
import uuid
from unittest.mock import patch
from pydantic import BaseModel
from datetime import datetime

from src.domain.entities.request.user import UserPlanningRequestEntity
from src.interface.adapter.serverless.api_gateway import UserPlanningRequestApiAdapter
from src.infrastructure.repositories.messaging_queue.sqs import SqsRepository
from src.infrastructure.repositories.database.dynamo.request_logging import RequestLoggingDynamoDBRepository


class AwsContextClass(BaseModel):
    aws_request_id: str


@pytest.fixture
def mock_event_api_gateway_request():
    return {
        'resource': '/api/guider/suggestion', 'path': '/api/guider/suggestion', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '17552', 'CloudFront-Viewer-Country': 'TH', 'Content-Type': 'application/json', 'Host': '7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com', 'Postman-Token': 'df1cf236-cee6-403f-ad22-5151c23fa769', 'User-Agent': 'PostmanRuntime/7.26.8', 'Via': '1.1 90cde83ad4a552d905b14cb6efc702b6.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'LG2pDsetqgC4sZ5lyVQJV2WoQf_mjRVabm6Iz2JoD83AkBjdDFy8kQ==', 'X-Amzn-Trace-Id': 'Root=1-643894b0-59281e52733836c351720d6f', 'X-Forwarded-For': '119.76.152.174, 130.176.148.160', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['17552'], 'CloudFront-Viewer-Country': ['TH'], 'Content-Type': ['application/json'], 'Host': ['7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com'], 'Postman-Token': ['df1cf236-cee6-403f-ad22-5151c23fa769'], 'User-Agent': ['PostmanRuntime/7.26.8'], 'Via': ['1.1 90cde83ad4a552d905b14cb6efc702b6.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['LG2pDsetqgC4sZ5lyVQJV2WoQf_mjRVabm6Iz2JoD83AkBjdDFy8kQ=='], 'X-Amzn-Trace-Id': ['Root=1-643894b0-59281e52733836c351720d6f'], 'X-Forwarded-For': ['119.76.152.174, 130.176.148.160'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'cxj4a8', 'resourcePath': '/api/guider/suggestion', 'httpMethod': 'POST', 'extendedRequestId': 'DVwrpFa7yQ0FsBw=', 'requestTime': '13/Apr/2023:23:48:00 +0000', 'path': '/Prod/api/guider/suggestion', 'accountId': '224320857919', 'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': '7ahyiahkei', 'requestTimeEpoch': 1681429680608, 'requestId': '88fb5d14-6f63-4690-8208-66f2047b6daf', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '119.76.152.174', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.26.8', 'user': None}, 'domainName': '7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com', 'apiId': '7ahyiahkei'},
        'body': '{\n  "place": "Bangkok",\n  "start_date": "2023-04-11T00:00:00.0Z",\n  "days": 3\n}',
        'isBase64Encoded': False
    }

@pytest.fixture
def mock_context_api_gateway_request():
    return AwsContextClass(aws_request_id='1234567890')

@patch.object(SqsRepository, 'publish')
@patch.object(RequestLoggingDynamoDBRepository, 'save_request_suggestion_entity')
@patch.object(uuid, 'uuid4')
def test_user_planning_request_api_adapter(mocker_uuid, mocker_request_logging_repository, mocker_sqs_request_repository, mock_event_api_gateway_request, mock_context_api_gateway_request):
    user_planning_request_api_adapter = UserPlanningRequestApiAdapter(
        event=mock_event_api_gateway_request, context=mock_context_api_gateway_request
    )
    user_uuid = 'aa46b814-b0ad-4238-a9bd-242d755510d4'

    mocker_uuid.return_value = user_uuid
        
    user_planning_request_api_adapter.execute()

    mocker_sqs_request_repository.assert_called_with({'user_id': user_uuid, 'request_id': '1234567890', 'place': 'Bangkok', 'days': 3, 'start_date': '2023-04-11T00:00:00'})
    mocker_request_logging_repository.assert_called_with(
        UserPlanningRequestEntity(request_id='1234567890', user_id=user_uuid, place='Bangkok', days=3, start_date=datetime(2023, 4, 11, 0, 0)), 
        'ACCEPTED'
    )
