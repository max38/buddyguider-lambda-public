import time
import boto3


class TripAdvisorDynamoDBRepository():
    
    def __init__(self) -> None:
        self.client = boto3.resource('dynamodb')
        self.table_location = self.client.Table('buddyguider_tripadvisor_location')

    def create_location(self, location_id: str, place_id: str, location_data: dict) -> dict:
        item = {
            'location_id': location_id,
            'place_id': place_id,
            'name': location_data.get('name'),
            'web_url': location_data.get('web_url'),
            'address_obj': location_data.get('address_obj'),
            'ancestors': location_data.get('ancestors'),
            'latitude': location_data.get('latitude'),
            'longitude': location_data.get('longitude'),
            'timezone': location_data.get('timezone'),
            'email': location_data.get('email'),
            'phone': location_data.get('phone'),
            'website': location_data.get('website'),
            'write_review': location_data.get('write_review'),
            'ranking_data': location_data.get('ranking_data'),
            'rating': location_data.get('rating'),
            'rating_image_url': location_data.get('rating_image_url'),
            'num_reviews': location_data.get('num_reviews'),
            'review_rating_count': location_data.get('review_rating_count'),
            'photo_count': location_data.get('photo_count'),
            'hours': location_data.get('hours'),
            'category': location_data.get('category'),
            'subcategory': location_data.get('subcategory'),
            'groups': location_data.get('groups'),
            'trip_types': location_data.get('trip_types'),
            'awards': location_data.get('awards'),
            'created_timestamp': int(time.time()),
            'updated_timestamp': int(time.time()),
        }
        self.table_location.put_item(Item=item)
        return item
    
    def get_location_by_id(self, location_id) -> dict:
        response = self.table_location.get_item(
            Key={
                'location_id': location_id
            }
        )
        if 'Item' in response:
            return response['Item']
        return None
    
    def update_location_photos_by_id(self, location_id: str, photos: dict):
        self.table_location.update_item(
            Key={
                'location_id': location_id
            },
            UpdateExpression='SET #photos = :photos, #updated_timestamp = :updated_timestamp',
            ExpressionAttributeNames={
                '#photos': 'photos',
                '#updated_timestamp': 'updated_timestamp',
            },
            ExpressionAttributeValues={
                ':photos': photos,
                ':updated_timestamp': int(time.time()),
            }
        )
    
    def update_location_by_id(self, location_id: str, place_id: str, location_data: dict) -> dict:
        self.table_location.update_item(
            Key={
                'location_id': location_id
            },
            UpdateExpression='SET #name = :name, #place_id = :place_id, #web_url = :web_url, #address_obj = :address_obj, #ancestors = :ancestors, #latitude = :latitude, #longitude = :longitude, #timezone = :timezone, #email = :email, #phone = :phone, #website = :website, #write_review = :write_review, #ranking_data = :ranking_data, #rating = :rating, #rating_image_url = :rating_image_url, #num_reviews = :num_reviews, #review_rating_count = :review_rating_count, #photo_count = :photo_count, #hours = :hours, #category = :category, #subcategory = :subcategory, #groups = :groups, #trip_types = :trip_types, #awards = :awards, #updated_timestamp = :updated_timestamp',
            ExpressionAttributeNames={
                '#place_id': 'place_id',
                '#name': 'name',
                '#web_url': 'web_url',
                '#address_obj': 'address_obj',
                '#ancestors': 'ancestors',
                '#latitude': 'latitude',
                '#longitude': 'longitude',
                '#timezone': 'timezone',
                '#email': 'email',
                '#phone': 'phone',
                '#website': 'website',
                '#write_review': 'write_review',
                '#ranking_data': 'ranking_data',
                '#rating': 'rating',
                '#rating_image_url': 'rating_image_url',
                '#num_reviews': 'num_reviews',
                '#review_rating_count': 'review_rating_count',
                '#photo_count': 'photo_count',
                '#hours': 'hours',
                '#category': 'category',
                '#subcategory': 'subcategory',
                '#groups': 'groups',
                '#trip_types': 'trip_types',
                '#awards': 'awards',
                '#updated_timestamp': 'updated_timestamp',
            },
            ExpressionAttributeValues={
                ':place_id': place_id,
                ':name': location_data.get('name'),
                ':web_url': location_data.get('web_url'),
                ':address_obj': location_data.get('address_obj'),
                ':ancestors': location_data.get('ancestors'),
                ':latitude': location_data.get('latitude'),
                ':longitude': location_data.get('longitude'),
                ':timezone': location_data.get('timezone'),
                ':email': location_data.get('email'),
                ':phone': location_data.get('phone'),
                ':website': location_data.get('website'),
                ':write_review': location_data.get('write_review'),
                ':ranking_data': location_data.get('ranking_data'),
                ':rating': location_data.get('rating'),
                ':rating_image_url': location_data.get('rating_image_url'),
                ':num_reviews': location_data.get('num_reviews'),
                ':review_rating_count': location_data.get('review_rating_count'),
                ':photo_count': location_data.get('photo_count'),
                ':category': location_data.get('category'),
                ':subcategory': location_data.get('subcategory'),
                ':groups': location_data.get('groups'),
                ':trip_types': location_data.get('trip_types'),
                ':awards': location_data.get('awards'),
                ':updated_timestamp': int(time.time()),
            }
        )
        return location_data
    
    def get_or_create_location_by_id(self, location_id: str, place_id: str, location_data: dict) -> dict:
        response = self.table_location.get_item(
            Key={
                'location_id': location_id
            }
        )
        if 'Item' in response:
            return response['Item']
        return self.create_location(location_id=location_id, place_id=place_id, location_data=location_data)
    
    def get_location_by_place_id(self, place_id: str) -> dict:
        response = self.table_location.query(
            IndexName='place_id-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('place_id').eq(place_id)
        )

        if 'Items' in response and len(response['Items']) > 0:
            return response['Items']
        return None
    