import boto3
import requests
from datetime import datetime
from urllib.parse import urlencode

from src.settings import TRIPADVISOR_API_KEY


class TripAdvisorRepository():

    rate_limit = 5000
    tripadvisor_api_key = TRIPADVISOR_API_KEY
    base_url = 'https://api.content.tripadvisor.com/api/'

    def __init__(self) -> None:
        self.dynamo_client = boto3.resource('dynamodb')
        self.request_db_table = self.dynamo_client.Table('buddyguider_tripadvisor_request')

    def request_get(self, url: str, params: dict=dict(), headers: dict=dict()):
        params['key'] = self.tripadvisor_api_key
        url = self.base_url + url + '?' + urlencode(params)
        headers['accept'] = 'application/json'
        headers['referer'] = 'https://buddyguider.com/'

        if not self.check_permission_to_call():
            return None

        response = requests.get(url, headers=headers)
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        
        print("response")
        print(url)
        print(response.status_code)
        print(response.json())
        return None
    
    def request_post(self, url: str, body: dict=dict(), params: dict=dict(), headers: dict=dict()):
        params['key'] = self.tripadvisor_api_key
        url = self.base_url + url + '?' + urlencode(params)
        headers['accept'] = 'application/json'
        headers['referer'] = 'https://buddyguider.com/'

        if not self.check_permission_to_call():
            return None

        response = requests.post(url, headers=headers, json=body)
        return response.json()
    
    def check_permission_to_call(self):
        month_slug = self.__get_current_month_slug()
        requested_count = self.get_request_count(month_slug)
        if requested_count is None:
            self.__create_request_count(month_slug)
            return True
        elif requested_count >= self.rate_limit:
            return False
        self.__update_request_count(month_slug)
        return True

    def get_request_count(self, month_slug: str):
        response = self.request_db_table.get_item(
            Key={
                'month_slug': month_slug
            }
        )
        if 'Item' in response:
            requested_count = response['Item']['requested_count']
            return requested_count
        return None
    
    @staticmethod
    def __get_current_month_slug():
        month_slug = '' + datetime.now().strftime('%Y-%m')
        return month_slug
    
    def __create_request_count(self, month_slug: str):
        self.request_db_table.put_item(
            Item={
                'month_slug': month_slug,
                'requested_count': 1
            }
        )
        return None
    
    def __update_request_count(self, month_slug: str):
        self.request_db_table.update_item(
            Key={
                'month_slug': month_slug
            },
            UpdateExpression='SET #requested_count = #requested_count + :increment',
            ExpressionAttributeNames={
                '#requested_count': 'requested_count'
            },
            ExpressionAttributeValues={
                ':increment': 1
            }
        )
        return None
