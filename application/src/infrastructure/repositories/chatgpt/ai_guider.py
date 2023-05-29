import json
import uuid
import time
import boto3
import requests
from urllib.parse import urlencode

from src.domain.repositories.place import PlaceRepository
from src.domain.repositories.ai_guider import AiRepository
from src.domain.entities.request.user import UserPlanningRequestEntity
from src.domain.entities.ai.travel_guider import TravelGuiderEntity, DailyDetailGuiderEntity, PlaceGuiderActivityEntity

from src.infrastructure.repositories.tripadvisor.guider import TripAdvisorGuiderRepository
from src.shared.convert import str_to_float_regex, dict_to_json

from src.settings import CHATGPT_API_TOKEN


class ChatGPTGuiderRepository(AiRepository):

    chatgpt_api_url = "https://api.openai.com/v1/"
    partner_place_information = TripAdvisorGuiderRepository()

    def __init__(self) -> None:
        self.dynamo_client = boto3.resource('dynamodb')
        self.request_db_table = self.dynamo_client.Table('buddyguider_chatgpt_request')

    def request_post(self, url: str, body: dict=dict(), params: dict=dict(), headers: dict=dict()):
        url = self.chatgpt_api_url + url + '?' + urlencode(params)
        headers['Authorization'] = f"Bearer {CHATGPT_API_TOKEN}"

        response = requests.post(url, headers=headers, json=body)
        response_data = response.json()

        self.request_db_table.put_item(
            Item={
                'api_request_id': response_data.get('id', str(uuid.uuid4())),
                # 'object': response_data.get('object'),
                # 'model': response_data.get('model'),
                # 'usage': response_data.get('usage'),
                'request_payload': dict_to_json(body),
                'response_status_code': int(response.status_code),
                'response_data': dict_to_json(response_data),
                'timestamp': int(time.time())
            }
        )

        return response_data

    def travel_planning_suggestion(self, user_planning_request: UserPlanningRequestEntity, place_repository: PlaceRepository = None) -> TravelGuiderEntity:
        payload = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": f"Please give me travel plan to visit {user_planning_request.place} in {str(user_planning_request.days)} days." + " and please return with json format like this ``` {\"day1\": [{\"activity\": \"...\", \"place_name\": \"...\", \"description\": \"...\", \"suggest_time_spend\": \"...\", \"country_name\": \"...\", \"province\": \"...\", \"map_location\": {\"lat\": \"..\", \"long\": \"..\"}}, {...}], \"day2\": [] } ```"
                }
            ]
        }
        response_data = self.request_post('chat/completions', body=payload)

        # response_data = self.__mock_response_data()
        travel_suggestion = self.__parse_travel_suggestion_response_data(user_planning_request, response_data)

        for day in travel_suggestion.daily_suggests:
            daily_detail = travel_suggestion.daily_suggests[day]
            activites = []

            for place_guider_activity in daily_detail.activites:
                place_guider_activity_full_information = self.__add_more_place_information(place_guider_activity, place_repository)
                activites.append(place_guider_activity_full_information)

                if place_guider_activity_full_information.place_id:
                    place_repository.update_increase_suggested_count_by_id(place_guider_activity_full_information.place_id)

            daily_detail.activites = activites

        return travel_suggestion
    
    def __add_more_place_information(self, place_guider_activity: PlaceGuiderActivityEntity, place_repository: PlaceRepository = None) -> PlaceGuiderActivityEntity:
        if not place_repository:
            return place_guider_activity
        
        place = place_repository.get_or_create_place_by_slug(place_guider_activity.place_slug, place_guider_activity)

        if not (len(place.trip_types) and len(place.photos)) and self.partner_place_information:
            place = self.partner_place_information.update_place_entity(place)
            place_repository.update_place_by_id(place.place_id, place)

        for place_field in ['place_id', 'address', 'rating', 'open_periods', 'phone_number', 'email', 'website', 'trip_types', 'types', 'photos']:
            setattr(place_guider_activity, place_field, getattr(place, place_field)) 
        print(place_guider_activity.dict())
        return place_guider_activity

    def __parse_travel_suggestion_response_data(self, user_planning_request: UserPlanningRequestEntity, response_data: dict) -> TravelGuiderEntity:
        suggestion_content = response_data['choices'][0]['message']['content']
        suggestion_content_data = json.loads(suggestion_content)
        print("--- suggestion_content_data ---")
        print(suggestion_content_data)

        daily_suggests = {}
        
        for day in suggestion_content_data:
            day_content_data = suggestion_content_data[day]
            activites = []
            
            for place_data in day_content_data:
                place_slug = f"{place_data['country_name']}-{place_data['province']}-{place_data['place_name']}".lower().replace(" ", "")
                place_guider_activity = PlaceGuiderActivityEntity(
                    place_slug=place_slug,
                    place_id=None,
                    address=None,
                    activity=place_data['activity'],
                    name=place_data['place_name'],
                    description=place_data['description'],
                    suggest_time_spend=place_data['suggest_time_spend'],
                    country_name=place_data['country_name'],
                    province=place_data['province'],
                    location_lat=str_to_float_regex(place_data['map_location']['lat']),
                    location_long=str_to_float_regex(place_data['map_location']['long']),
                    types=[],
                    open_periods=[],
                    trip_types=[],
                    photos=[],
                )

                activites.append(place_guider_activity)

            daily_suggests[day] = DailyDetailGuiderEntity(
                day=int(day.replace("day", "")),
                description="",
                activites=activites,
            )

        travel_suggestion = TravelGuiderEntity(
            request_id=user_planning_request.request_id,
            user_id=user_planning_request.user_id,
            place=user_planning_request.place,
            days=user_planning_request.days,
            start_date=user_planning_request.start_date,
            message=response_data,
            daily_suggests=daily_suggests,
        )

        return travel_suggestion

    def __mock_response_data(self):
        return {
            'id': 'chatcmpl-75OsrXoDGBipmtDGm57o5382aEvXf',
            'object': 'chat.completion',
            'created': 1681521649,
            'model': 'gpt-3.5-turbo-0301',
            'usage': {'prompt_tokens': 93, 'completion_tokens': 1003, 'total_tokens': 1096},
            'choices': [
                {
                    'message': {
                        'role': 'assistant', 
                        'content': '{\n  "day1": [\n    {\n      "activity": "Visit Tokyo Tower",\n      "place_name": "Tokyo Tower",\n      "description": "Tokyo Tower is a communications and observation tower located in the Shiba-koen district of Minato, Tokyo, Japan.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6586",\n        "long": "139.7454"\n      }\n    },\n    {\n      "activity": "Explore Senso-ji Temple",\n      "place_name": "Senso-ji Temple",\n      "description": "Senso-ji is an ancient Buddhist temple located in Asakusa, Tokyo, Japan.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.7147",\n        "long": "139.7967"\n      }\n    },\n    {\n      "activity": "Experience Shibuya Crossing",\n      "place_name": "Shibuya Crossing",\n      "description": "Shibuya Crossing is one of the busiest intersections in the world, located in Shibuya, Tokyo, Japan.",\n      "suggest_time_spend": "1-2 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6595",\n        "long": "139.7003"\n      }\n    }\n  ],\n  "day2": [\n    {\n      "activity": "Visit Meiji Shrine",\n      "place_name": "Meiji Shrine",\n      "description": "Meiji Shrine is a Shinto shrine located in Shibuya, Tokyo, Japan.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6764",\n        "long": "139.6992"\n      }\n    },\n    {\n      "activity": "Explore Harajuku",\n      "place_name": "Harajuku",\n      "description": "Harajuku is a district in Shibuya, known for its fashion and street culture.",\n      "suggest_time_spend": "3-4 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6719",\n        "long": "139.7101"\n      }\n    },\n    {\n      "activity": "Visit Tokyo National Museum",\n      "place_name": "Tokyo National Museum",\n      "description": "The Tokyo National Museum is the oldest and largest museum in Japan, located in Ueno, Tokyo.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.7187",\n        "long": "139.7748"\n      }\n    }\n  ],\n  "day3": [\n    {\n      "activity": "Visit Tsukiji Fish Market",\n      "place_name": "Tsukiji Fish Market",\n      "description": "Tsukiji Fish Market is the largest wholesale fish and seafood market in the world, located in Tsukiji, Tokyo, Japan.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6654",\n        "long": "139.7706"\n      }\n    },\n    {\n      "activity": "Explore Akihabara",\n      "place_name": "Akihabara",\n      "description": "Akihabara is a district in Tokyo known for its electronics, anime, and gaming culture.",\n      "suggest_time_spend": "3-4 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6990",\n        "long": "139.7710"\n      }\n    },\n    {\n      "activity": "Visit Imperial Palace",\n      "place_name": "Imperial Palace",\n      "description": "The Imperial Palace is the primary residence of the Emperor of Japan, located in Chiyoda, Tokyo, Japan.",\n      "suggest_time_spend": "2-3 hours",\n      "country_name": "Japan",\n      "province": "Tokyo",\n      "map_location": {\n        "lat": "35.6829",\n        "long": "139.7531"\n      }\n    }\n  ]\n}'
                    }, 
                    'finish_reason': 'stop', 
                    'index': 0
                }
            ]
        }
