from src.domain.entities.place import PlaceEntity, PlaceOpenPeriodEntity

from src.infrastructure.repositories.tripadvisor.api import TripAdvisorLocationAPIRepository
from src.infrastructure.repositories.database.dynamo.tripadvisor import TripAdvisorDynamoDBRepository

from src.shared.convert import str_to_float_regex


class TripAdvisorGuiderRepository():

    def __init__(self) -> None:
        self.db_repository = TripAdvisorDynamoDBRepository()
        self.api_repository = TripAdvisorLocationAPIRepository()

    def update_place_entity(self, place: PlaceEntity):
        locations = self.db_repository.get_location_by_place_id(place_id=place.place_id)
        
        if locations:
            location_detail = locations[0] # need logic selection
        else:
            location_detail = self.__get_location_api(place=place)

        if location_detail:
            place = self.__update_place_entity(place=place, location_detail=location_detail)
        return place

    def __update_place_entity(self, place: PlaceEntity, location_detail: dict) -> PlaceEntity:
        if 'rating' in location_detail:
            place.rating = str_to_float_regex(location_detail['rating'])

        if 'address_obj' in location_detail:
            place.address = location_detail['address_obj']['address_string']

        if 'hours' in location_detail:
            open_periods = location_detail['hours']
            place.open_periods = []

            for period in open_periods['periods']:
                place_period = PlaceOpenPeriodEntity(
                    open_day=period['open']['day'],
                    open_time=period['open']['time'],
                    close_day=period['close']['day'],
                    close_time=period['close']['time'],
                    timezone=location_detail['timezone']
                )
                place.open_periods.append(place_period)

        place.phone_number = location_detail.get('phone', '')
        place.email = location_detail.get('email', '')
        place.website = location_detail.get('website', '')
        
        place.trip_types = []
        for trip_type in location_detail['trip_types']:
            place.trip_types.append(trip_type['name'])

        place_types = []
        for subcategory in location_detail['subcategory']:
            place_types.append(subcategory['name'])
            
        if 'name' in location_detail['category']:
            place_types.append(location_detail['category']['name'])
        
        place.types = list(set(place_types))

        # photos
        for photo_data in location_detail['photos']:
            if 'original' in photo_data['images']:
                place.photos.append(photo_data['images']['original']['url'])
            elif 'large' in photo_data['images']:
                place.photos.append(photo_data['images']['large']['url'])
            elif 'medium' in photo_data['images']:
                place.photos.append(photo_data['images']['medium']['url'])
        place.photos = list(set(place.photos))

        return place

    def __get_location_api(self, place: PlaceEntity) -> dict:
        search_location_results = self.api_repository.location_search_by_place(place=place)
        
        if not search_location_results:
            return None
        
        location = search_location_results[0]
        location_id = location['location_id']
        location_detail = self.api_repository.get_location_detail(location_id=location_id)

        if location_detail:
            self.__update_db_location_data(location_id=location_id, location_detail=location_detail, place=place)
            location_photos = self.api_repository.get_location_photos(location_id=location_id)
            self.db_repository.update_location_photos_by_id(location_id=location_id, photos=location_photos['data'])
            location_detail['photos'] = location_photos['data']

        return location_detail
        
    def __update_db_location_data(self, location_id: str, location_detail: dict, place: PlaceEntity):
        self.db_repository.create_location(
            location_id=location_id,
            place_id=place.place_id,
            location_data=location_detail
        )