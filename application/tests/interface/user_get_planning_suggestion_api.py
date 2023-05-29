import pytest
from unittest.mock import patch
from pydantic import BaseModel
from src.interface.adapter.serverless.api_gateway import GetSuggestionResultApiAdapter


class AwsContextClass(BaseModel):
    aws_request_id: str


@pytest.fixture
def mock_event_api_gateway_request():
    return {
        'resource': '/api/guider/suggestion/{request_id}', 
        'path': '/api/guider/suggestion/e787861c-f831-4f60-8fc6-a2743d7a47a5', 
        'httpMethod': 'GET', 
        'headers': {
            'Accept': '*/*', 
            'Accept-Encoding': 'gzip, deflate, br', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 
            'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 
            'CloudFront-Viewer-ASN': '17552', 'CloudFront-Viewer-Country': 'TH', 'Host': '7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com', 
            'Postman-Token': '8a9fb90e-59e4-4aa7-8ebe-311c5ad484fe', 'User-Agent': 'PostmanRuntime/7.26.8', 
            'Via': '1.1 f9b9c1399f061e6d3016b151b0a94748.cloudfront.net (CloudFront)', 
            'X-Amz-Cf-Id': '3cjyN8m25sYvLoIyT3Zc19C8Z-UaTJeLhe-uZs8kUeVwSDx7A2XcsA==', 
            'X-Amzn-Trace-Id': 'Root=1-643b3e7d-153ef84e4349fff51a8952a3', 'X-Forwarded-For': '119.76.152.174, 130.176.148.71', 
            'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'
        }, 
        'multiValueHeaders': {
            'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'CloudFront-Forwarded-Proto': ['https'], 
            'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 
            'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['17552'], 'CloudFront-Viewer-Country': ['TH'], 
            'Host': ['7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com'], 'Postman-Token': ['8a9fb90e-59e4-4aa7-8ebe-311c5ad484fe'], 
            'User-Agent': ['PostmanRuntime/7.26.8'], 'Via': ['1.1 f9b9c1399f061e6d3016b151b0a94748.cloudfront.net (CloudFront)'], 
            'X-Amz-Cf-Id': ['3cjyN8m25sYvLoIyT3Zc19C8Z-UaTJeLhe-uZs8kUeVwSDx7A2XcsA=='], 
            'X-Amzn-Trace-Id': ['Root=1-643b3e7d-153ef84e4349fff51a8952a3'], 'X-Forwarded-For': ['119.76.152.174, 130.176.148.71'], 
            'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']
        }, 
        'queryStringParameters': None, 
        'multiValueQueryStringParameters': None, 
        'pathParameters': {'request_id': 'e787861c-f831-4f60-8fc6-a2743d7a47a5'}, 
        'stageVariables': None, 
        'requestContext': {
            'resourceId': 'zipr65', 'resourcePath': '/api/guider/suggestion/{request_id}', 'httpMethod': 'GET', 'extendedRequestId': 
            'DcazqEsPSQ0Fuug=', 'requestTime': '16/Apr/2023:00:17:01 +0000', 
            'path': '/Prod/api/guider/suggestion/e787861c-f831-4f60-8fc6-a2743d7a47a5', 'accountId': '224320857919', 
            'protocol': 'HTTP/1.1', 'stage': 'Prod', 'domainPrefix': '7ahyiahkei', 'requestTimeEpoch': 1681604221563, 
            'requestId': '12d12a06-2db1-42f0-b45a-f27942025678', 
            'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '119.76.152.174', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.26.8', 'user': None
                         }, 
            'domainName': '7ahyiahkei.execute-api.ap-southeast-1.amazonaws.com', 'apiId': '7ahyiahkei'
        }, 
        'body': None, 'isBase64Encoded': False
    }

@pytest.fixture
def mock_context_api_gateway_request():
    return AwsContextClass(aws_request_id='1234567890')



def test_user_get_planning_suggestion_api_adapter(
        mock_event_api_gateway_request, mock_context_api_gateway_request
    ):
    user_get_planning_suggestion_api_adapter = GetSuggestionResultApiAdapter(
        event=mock_event_api_gateway_request, context=mock_context_api_gateway_request
    )
    response = user_get_planning_suggestion_api_adapter.execute()
    print(response)
    assert response['statusCode'] == 200
    assert response['body'] == '{"request_id": "e787861c-f831-4f60-8fc6-a2743d7a47a5", "status": "success", "data": {"suggestion": {"suggestion_id": "e787861c-f831-4f60-8fc6-a2743d7a47a5", "suggestion_name": "suggestion_name", "suggestion_description": "suggestion_description", "suggestion_image": "suggestion_image", "suggestion_type": "suggestion_type", "suggestion_location": "suggestion_location", "suggestion_price": "suggestion_price", "suggestion_rating": "suggestion_rating", "suggestion_opening_hours": "suggestion_opening_hours", "suggestion_website": "suggestion_website", "suggestion_phone_number": "suggestion_phone_number", "suggestion_lat": "suggestion_lat", "suggestion_lng": "suggestion_lng", "suggestion_created_at": "suggestion_created_at", "suggestion_updated_at": "suggestion_updated_at", "suggestion_deleted_at": "suggestion_deleted_at"}}}'
    assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}


def test_user_get_planning_suggestion_api_status_fail():
    user_get_planning_suggestion_api_adapter = GetSuggestionResultApiAdapter(
        event={}, context={}
    )
    response = user_get_planning_suggestion_api_adapter.execute()
    assert response['statusCode'] == 400
    assert response['body'] == '{"request_id": "", "status": "fail", "data": {"error": "Bad Request"}}'
    assert response['headers'] == {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    