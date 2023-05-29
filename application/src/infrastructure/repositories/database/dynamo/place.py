import boto3
import uuid
import time

from src.domain.entities.place import PlaceEntity
from src.domain.repositories.place import PlaceRepository

from src.shared.convert import float_to_decimal


class PlaceDynamoDBRepository(PlaceRepository):

    def __init__(self) -> None:
        self.client = boto3.resource('dynamodb')
        self.table = self.client.Table('buddyguider_place')

    def create_place(self, place: PlaceEntity) -> PlaceEntity:
        item = {
            'place_id': str(uuid.uuid4()),
            'place_slug': place.place_slug,
            'name': place.name,
            'address': place.address if place.address else '',
            'location_lat': float_to_decimal(place.location_lat),
            'location_long': float_to_decimal(place.location_long),
            'country_name': place.country_name,
            'province': place.province,
            'rating': float_to_decimal(place.rating),
            'open_periods': place.open_periods.dict() if place.open_periods else [],
            'photos': place.photos if place.photos else [],
            'trip_types': place.trip_types if place.trip_types else [],
            'phone_number': place.phone_number if place.phone_number else '',
            'email': place.email if place.email else '',
            'website': place.website if place.website else '',
            'types': place.types,
            'description': place.description if place.description else '',
            'suggested_count': 0,
            'created_timestamp': int(time.time()),
            'updated_timestamp': int(time.time()),
        }
        self.table.put_item(Item=item)
        return PlaceEntity(**item)

    def get_place_by_id(self, place_id: str) -> PlaceEntity:
        response = self.table.get_item(
            Key={
                'place_id': place_id
            }
        )
        if 'Item' in response:
            return PlaceEntity(**response['Item'])
        return None
    
    def update_increase_suggested_count_by_id(self, place_id: str) -> None:
        try:
            self.table.update_item(
                Key={
                    'place_id': place_id
                },
                UpdateExpression='SET #suggested_count = #suggested_count + :increment',
                ExpressionAttributeNames={
                    '#suggested_count': 'suggested_count'
                },
                ExpressionAttributeValues={
                    ':increment': 1
                }
            )
        except Exception as e:
            self.table.update_item(
                Key={
                    'place_id': place_id
                },
                UpdateExpression='SET #suggested_count = :suggested_count',
                ExpressionAttributeNames={
                    '#suggested_count': 'suggested_count'
                },
                ExpressionAttributeValues={
                    ':suggested_count': 1
                }
            )
        return None
    
    def get_place_by_slug(self, place_slug: str) -> PlaceEntity:
        response = self.table.query(
            IndexName='place_slug-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('place_slug').eq(place_slug)
        )
        if 'Items' in response and len(response['Items']) > 0:
            return PlaceEntity(**response['Items'][0])
        return None
    
    def update_place_by_id(self, place_id: str, place: PlaceEntity) -> PlaceEntity:
        self.table.update_item(
            Key={
                'place_id': place_id
            },
            UpdateExpression='SET #place_slug = :place_slug, #updated_timestamp = :updated_timestamp, #name = :name, #address = :address, #location_lat = :location_lat, #location_long = :location_long, #country_name = :country_name, #province = :province, #rating = :rating, #open_periods = :open_periods, #photos = :photos, #types = :types, #trip_types = :trip_types, #phone_number = :phone_number, #email = :email, #website = :website, #description = :description',
            ExpressionAttributeNames={
                '#place_slug': 'place_slug',
                '#name': 'name',
                '#address': 'address',
                '#location_lat': 'location_lat',
                '#location_long': 'location_long',
                '#country_name': 'country_name',
                '#province': 'province',
                '#rating': 'rating',
                '#open_periods': 'open_periods',
                '#photos': 'photos',
                '#trip_types': 'trip_types',
                '#phone_number': 'phone_number',
                '#email': 'email',
                '#website': 'website',
                '#types': 'types',
                '#description': 'description',
                '#updated_timestamp': 'updated_timestamp',
            },
            ExpressionAttributeValues={
                ':place_slug': place.place_slug,
                ':name': place.name,
                ':address': place.address if place.address else '',
                ':location_lat': float_to_decimal(place.location_lat),
                ':location_long': float_to_decimal(place.location_long),
                ':country_name': place.country_name,
                ':province': place.province,
                ':rating': float_to_decimal(place.rating),
                ':open_periods': [period.dict() for period in place.open_periods],
                ':photos': place.photos if place.photos else [],
                ':trip_types': place.trip_types if place.trip_types else [],
                ':phone_number': place.phone_number if place.phone_number else '',
                ':email': place.email if place.email else '',
                ':website': place.website if place.website else '',
                ':types': place.types,
                ':description': place.description if place.description else '',
                ':updated_timestamp': int(time.time())
            }
        )
        return place
    
    def get_or_create_place_by_slug(self, place_slug: str, place: PlaceEntity) -> PlaceEntity:
        response = self.table.query(
            IndexName='place_slug-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('place_slug').eq(place_slug)
        )

        if 'Items' in response and len(response['Items']) > 0:
            return PlaceEntity(**response['Items'][0])
        else:
            place.place_id = str(uuid.uuid4())
            return self.create_place(place)
    
    def update_or_create_place_by_slug(self, place_slug: str, place: PlaceEntity) -> PlaceEntity:
        response = self.table.query(
            IndexName='place_slug-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('place_slug').eq(place_slug)
        )

        if 'Items' in response and len(response['Items']) > 0:
            for item in response['Items']:
                place.place_id = item['place_id']
                self.update_place_by_id(place.place_id, place)

            return place
        else:
            place.place_id = str(uuid.uuid4())
            return self.create_place(place)
