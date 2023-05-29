import boto3
import time
import json

from src.domain.repositories.place import PlaceRepository
from src.domain.repositories.request_logging import RequestLoggingRepository
from src.domain.entities.request.user import UserPlanningRequestEntity, UserPlanningSuggestionResponseEntity
from src.domain.entities.place import PlaceEntity, PlaceOpenPeriodEntity
from src.domain.entities.ai.travel_guider import TravelGuiderEntity, DailyDetailGuiderEntity, PlaceGuiderActivityEntity

from src.settings import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY
from src.shared.convert import dict_to_json, datetime_to_str_iso_datetime


class RequestLoggingDynamoDBRepository(RequestLoggingRepository):

    def __init__(self, place_repository: PlaceRepository = None) -> None:
        self.client = boto3.resource(
            'dynamodb',
            region_name=AWS_REGION,
            # aws_access_key_id=AWS_ACCESS_KEY_ID,
            # aws_secret_access_key=AWS_ACCESS_SECRET_KEY,
        )
        self.table = self.client.Table('buddyguider_request_suggestion')
        self.place_repository = place_repository

    def get_suggestion_request(self, request_id: str) -> dict:
        response = self.table.get_item(
            Key={
                'request_id': request_id
            }
        )
        if not response['Item']:
            return None
        response_item = response['Item']
        # response_item = self.__mock_response_request_suggestion()
        suggestion_response = UserPlanningSuggestionResponseEntity(
            request_id=response_item['request_id'],
            user_id=response_item['user_id'],
            status=response_item['status'],
            requested_place=response_item['requested_place'],
            requested_days=response_item['requested_days'],
            requested_start_date=response_item['requested_start_date'],
            requested_timestamp=response_item['requested_timestamp'],
            timestamp=response_item['timestamp'],
        )
        if 'result' in response_item:
            result_data = json.loads(response_item['result'])
            daily_suggests = {}
            for day, daily_data in result_data['daily_suggests'].items():
                activites = []
                for activity in daily_data['activites']:
                    if self.place_repository and False:
                        # Query place database
                        pass
                    else:
                        open_periods = [
                            PlaceOpenPeriodEntity(
                                open_day=period['open_day'],
                                open_time=period['open_time'],
                                close_day=period['close_day'],
                                close_time=period['close_time'],
                                timezone=period['timezone'],
                            ) for period in activity.get('open_periods', [])
                        ]
                        activites.append(PlaceGuiderActivityEntity(
                            place_slug=activity['place_slug'],
                            name=activity['name'],
                            activity=activity['activity'],
                            description=activity['description'],
                            place_id=activity['place_id'],
                            address=activity['address'],
                            location_lat=activity['location_lat'],
                            location_long=activity['location_long'],
                            country_name=activity['country_name'],
                            province=activity['province'],
                            types=activity['types'],
                            suggest_time_spend=activity['suggest_time_spend'],
                            rating=activity.get('rating', 0),
                            open_periods=open_periods,
                            trip_types=activity.get('trip_types', []),
                            photos=activity.get('photos', []),
                            phone_number=activity.get('phone_number', ''),
                            email=activity.get('email', ''),
                            website=activity.get('website', ''),
                        ))
                daily_suggests[day] = DailyDetailGuiderEntity(
                    day=daily_data['day'],
                    description=daily_data['description'],
                    activites=activites
                )
            suggestion_response.result = TravelGuiderEntity(
                place=result_data['place'],
                days=result_data['days'],
                start_date=result_data['start_date'],
                request_id=result_data['request_id'],
                user_id=result_data['user_id'],
                # message=result_data['message'],
                message={},
                daily_suggests=daily_suggests
            )

        return suggestion_response
    
    def save_request_suggestion_entity(self, user_request_planning: UserPlanningRequestEntity, status: str):
        item = {
            'request_id': user_request_planning.request_id,
            'user_id': user_request_planning.user_id,
            'status': status,
            'requested_place': user_request_planning.place,
            'requested_days': user_request_planning.days,
            'requested_start_date': datetime_to_str_iso_datetime(user_request_planning.start_date),
            'requested_timestamp': int(time.time()),
            'timestamp': int(time.time()),
        }
        self.table.put_item(Item=item)

    def update_request_suggestion_status(self, user_request_planning: UserPlanningRequestEntity, status: str):
        self.table.update_item(
            Key={
                'request_id': user_request_planning.request_id
            },
            UpdateExpression='SET #status = :status, #timestamp = :timestamp',
            ExpressionAttributeNames={
                '#status': 'status',
                '#timestamp': 'timestamp'
            },
            ExpressionAttributeValues={
                ':status': status,
                ':timestamp': int(time.time())
            },
            ReturnValues='UPDATED_NEW'
        )

    def update_request_suggestion_complete(self, user_request_planning: UserPlanningRequestEntity, travel_guider: TravelGuiderEntity):
        self.table.update_item(
            Key={
                'request_id': user_request_planning.request_id
            },
            UpdateExpression='SET #status = :status, #timestamp = :timestamp, #result = :result',
            ExpressionAttributeNames={
                '#status': 'status',
                '#timestamp': 'timestamp',
                '#result': 'result'
            },
            ExpressionAttributeValues={
                ':status': 'COMPLETED',
                ':timestamp': int(time.time()),
                ':result': dict_to_json(travel_guider.dict())
            }
        )

    def update_request_suggestion_error(self, user_request_planning: UserPlanningRequestEntity, error: Exception):
        self.table.update_item(
            Key={
                'request_id': user_request_planning.request_id
            },
            UpdateExpression='SET #status = :status, #timestamp = :timestamp, #error_message = :error_message',
            ExpressionAttributeNames={
                '#status': 'status',
                '#timestamp': 'timestamp',
                '#error_message': 'error_message'
            },
            ExpressionAttributeValues={
                ':status': 'ERROR',
                ':timestamp': int(time.time()),
                ':error_message': str(error)
            }
        )

    def __mock_response_request_suggestion(self) -> dict:
        return {
            "requested_place": "Tokyo",
            "requested_start_date": "2023-04-22T00:10:00.000000Z",
            "user_id": "f1050d9e-3113-4f53-9142-fbfb9fe5eb56",
            "request_id": "e787861c-f831-4f60-8fc6-a2743d7a47a5",
            "status": "COMPLETED",
            "timestamp": 1681560843.0,
            "requested_timestamp": 1681560238.0,
            "requested_days": 3.0,
            "result": "{\"request_id\": \"e787861c-f831-4f60-8fc6-a2743d7a47a5\", \"user_id\": \"f1050d9e-3113-4f53-9142-fbfb9fe5eb56\", \"place\": \"Tokyo\", \"days\": 3, \"start_date\": \"2023-04-22T00:10:00\", \"message\": {\"id\": \"chatcmpl-75OsrXoDGBipmtDGm57o5382aEvXf\", \"object\": \"chat.completion\", \"created\": 1681521649, \"model\": \"gpt-3.5-turbo-0301\", \"usage\": {\"prompt_tokens\": 93, \"completion_tokens\": 1003, \"total_tokens\": 1096}, \"choices\": [{\"message\": {\"role\": \"assistant\", \"content\": \"{\\n  \\\"day1\\\": [\\n    {\\n      \\\"activity\\\": \\\"Visit Tokyo Tower\\\",\\n      \\\"place_name\\\": \\\"Tokyo Tower\\\",\\n      \\\"description\\\": \\\"Tokyo Tower is a communications and observation tower located in the Shiba-koen district of Minato, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6586\\\",\\n        \\\"long\\\": \\\"139.7454\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Explore Senso-ji Temple\\\",\\n      \\\"place_name\\\": \\\"Senso-ji Temple\\\",\\n      \\\"description\\\": \\\"Senso-ji is an ancient Buddhist temple located in Asakusa, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.7147\\\",\\n        \\\"long\\\": \\\"139.7967\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Experience Shibuya Crossing\\\",\\n      \\\"place_name\\\": \\\"Shibuya Crossing\\\",\\n      \\\"description\\\": \\\"Shibuya Crossing is one of the busiest intersections in the world, located in Shibuya, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"1-2 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6595\\\",\\n        \\\"long\\\": \\\"139.7003\\\"\\n      }\\n    }\\n  ],\\n  \\\"day2\\\": [\\n    {\\n      \\\"activity\\\": \\\"Visit Meiji Shrine\\\",\\n      \\\"place_name\\\": \\\"Meiji Shrine\\\",\\n      \\\"description\\\": \\\"Meiji Shrine is a Shinto shrine located in Shibuya, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6764\\\",\\n        \\\"long\\\": \\\"139.6992\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Explore Harajuku\\\",\\n      \\\"place_name\\\": \\\"Harajuku\\\",\\n      \\\"description\\\": \\\"Harajuku is a district in Shibuya, known for its fashion and street culture.\\\",\\n      \\\"suggest_time_spend\\\": \\\"3-4 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6719\\\",\\n        \\\"long\\\": \\\"139.7101\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Visit Tokyo National Museum\\\",\\n      \\\"place_name\\\": \\\"Tokyo National Museum\\\",\\n      \\\"description\\\": \\\"The Tokyo National Museum is the oldest and largest museum in Japan, located in Ueno, Tokyo.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.7187\\\",\\n        \\\"long\\\": \\\"139.7748\\\"\\n      }\\n    }\\n  ],\\n  \\\"day3\\\": [\\n    {\\n      \\\"activity\\\": \\\"Visit Tsukiji Fish Market\\\",\\n      \\\"place_name\\\": \\\"Tsukiji Fish Market\\\",\\n      \\\"description\\\": \\\"Tsukiji Fish Market is the largest wholesale fish and seafood market in the world, located in Tsukiji, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6654\\\",\\n        \\\"long\\\": \\\"139.7706\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Explore Akihabara\\\",\\n      \\\"place_name\\\": \\\"Akihabara\\\",\\n      \\\"description\\\": \\\"Akihabara is a district in Tokyo known for its electronics, anime, and gaming culture.\\\",\\n      \\\"suggest_time_spend\\\": \\\"3-4 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6990\\\",\\n        \\\"long\\\": \\\"139.7710\\\"\\n      }\\n    },\\n    {\\n      \\\"activity\\\": \\\"Visit Imperial Palace\\\",\\n      \\\"place_name\\\": \\\"Imperial Palace\\\",\\n      \\\"description\\\": \\\"The Imperial Palace is the primary residence of the Emperor of Japan, located in Chiyoda, Tokyo, Japan.\\\",\\n      \\\"suggest_time_spend\\\": \\\"2-3 hours\\\",\\n      \\\"country_name\\\": \\\"Japan\\\",\\n      \\\"province\\\": \\\"Tokyo\\\",\\n      \\\"map_location\\\": {\\n        \\\"lat\\\": \\\"35.6829\\\",\\n        \\\"long\\\": \\\"139.7531\\\"\\n      }\\n    }\\n  ]\\n}\"}, \"finish_reason\": \"stop\", \"index\": 0}]}, \"daily_suggests\": {\"day1\": {\"activites\": [{\"place_slug\": \"japan-tokyo-tokyotower\", \"place_id\": \"343a96f6-ccfd-4edd-9f51-1f78cd7e469d\", \"name\": \"Tokyo Tower\", \"address\": null, \"location_lat\": 35.6586, \"location_long\": 139.7454, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Tokyo Tower is a communications and observation tower located in the Shiba-koen district of Minato, Tokyo, Japan.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Visit Tokyo Tower\"}, {\"place_slug\": \"japan-tokyo-senso-jitemple\", \"place_id\": \"ab4c67bf-b4c3-4646-9974-695a4522e8a6\", \"name\": \"Senso-ji Temple\", \"address\": \"\", \"location_lat\": 35.7147, \"location_long\": 139.7967, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Senso-ji is an ancient Buddhist temple located in Asakusa, Tokyo, Japan.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Explore Senso-ji Temple\"}, {\"place_slug\": \"japan-tokyo-shibuyacrossing\", \"place_id\": \"36e276ac-24a3-4693-af23-a79d4a75afcd\", \"name\": \"Shibuya Crossing\", \"address\": \"\", \"location_lat\": 35.6595, \"location_long\": 139.7003, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Shibuya Crossing is one of the busiest intersections in the world, located in Shibuya, Tokyo, Japan.\", \"suggest_time_spend\": \"1-2 hours\", \"activity\": \"Experience Shibuya Crossing\"}], \"description\": \"\", \"day\": 1}, \"day2\": {\"activites\": [{\"place_slug\": \"japan-tokyo-meijishrine\", \"place_id\": \"9947dd01-2017-4998-a985-a99140daaf1a\", \"name\": \"Meiji Shrine\", \"address\": \"\", \"location_lat\": 35.6764, \"location_long\": 139.6992, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Meiji Shrine is a Shinto shrine located in Shibuya, Tokyo, Japan.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Visit Meiji Shrine\"}, {\"place_slug\": \"japan-tokyo-harajuku\", \"place_id\": \"1f481659-ea7c-4a44-9c95-c63994324248\", \"name\": \"Harajuku\", \"address\": \"\", \"location_lat\": 35.6719, \"location_long\": 139.7101, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Harajuku is a district in Shibuya, known for its fashion and street culture.\", \"suggest_time_spend\": \"3-4 hours\", \"activity\": \"Explore Harajuku\"}, {\"place_slug\": \"japan-tokyo-tokyonationalmuseum\", \"place_id\": \"13fb90d6-a5c0-4eb8-880a-ed10b16d4cb3\", \"name\": \"Tokyo National Museum\", \"address\": \"\", \"location_lat\": 35.7187, \"location_long\": 139.7748, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"The Tokyo National Museum is the oldest and largest museum in Japan, located in Ueno, Tokyo.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Visit Tokyo National Museum\"}], \"description\": \"\", \"day\": 2}, \"day3\": {\"activites\": [{\"place_slug\": \"japan-tokyo-tsukijifishmarket\", \"place_id\": \"e369e197-bd97-4556-9aea-c5d82d9f0fb3\", \"name\": \"Tsukiji Fish Market\", \"address\": \"\", \"location_lat\": 35.6654, \"location_long\": 139.7706, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Tsukiji Fish Market is the largest wholesale fish and seafood market in the world, located in Tsukiji, Tokyo, Japan.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Visit Tsukiji Fish Market\"}, {\"place_slug\": \"japan-tokyo-akihabara\", \"place_id\": \"4475060d-c1bf-47eb-bd98-6ecc91d1275e\", \"name\": \"Akihabara\", \"address\": \"\", \"location_lat\": 35.699, \"location_long\": 139.771, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"Akihabara is a district in Tokyo known for its electronics, anime, and gaming culture.\", \"suggest_time_spend\": \"3-4 hours\", \"activity\": \"Explore Akihabara\"}, {\"place_slug\": \"japan-tokyo-imperialpalace\", \"place_id\": \"e7a962c4-1890-4a09-9518-dbdb77da9548\", \"name\": \"Imperial Palace\", \"address\": \"\", \"location_lat\": 35.6829, \"location_long\": 139.7531, \"country_name\": \"Japan\", \"province\": \"Tokyo\", \"types\": [], \"description\": \"The Imperial Palace is the primary residence of the Emperor of Japan, located in Chiyoda, Tokyo, Japan.\", \"suggest_time_spend\": \"2-3 hours\", \"activity\": \"Visit Imperial Palace\"}], \"description\": \"\", \"day\": 3}}}"
        }
