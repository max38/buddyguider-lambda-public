import requests
import urllib.parse

from src.infrastructure.repositories.googleapi.base import GoogleAPIRepository


class GooglePlaceAPIRepository(GoogleAPIRepository):
    base_url = 'https://maps.googleapis.com/maps/api/'
    
    def find_place_from_text(self, place_name: str, language: str='en'):
        fields = 'business_status,formatted_address,geometry,icon,icon_mask_base_uri,icon_background_color,name,photo,place_id,plus_code,type,opening_hours'
        fields = urllib.parse.quote(fields)
        url_request = f'{self.base_url}place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields={fields}&key={self.google_api_key}&language={language}'
        response = requests.get(url_request)
        response_data = response.json()

        # https://maps.googleapis.com/maps/api/place/photo?maxwidth=3000&photo_reference=AZose0nodgCk3fQWOg-kEHRXBJmuEBP3EZWOtaOQBmSFWhrnjSbRKgRjStH6pwApw07FEiOcEuuZ7JpS0d7pPB89V7YWcJO7IkwaNTGfI6kccemutHX1tJbD9Yl3Av-od0vVCfqr3tIt82JLMulMWTvcSMW5fxIDmTwqqXvd3ytYoin41lB7&key=AIzaSyCx8B-LABUS17J3fluVFhgEFY7V5nAHloQ

        # {'candidates': [{'business_status': 'OPERATIONAL', 'formatted_address': '991 Rama I Rd, Pathum Wan, Bangkok 10330, Thailand', 'geometry': {'location': {'lat': 13.7462411, 'lng': 100.5347402}, 'viewport': {'northeast': {'lat': 13.74856255, 'lng': 100.53709195}, 'southwest': {'lat': 13.74461955, 'lng': 100.53273455}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/shopping-71.png', 'icon_background_color': '#4B96F3', 'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/shopping_pinlet', 'name': 'Siam Paragon', 'photos': [{'height': 4624, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/110838996163657732339">A Google User</a>'], 'photo_reference': 'AZose0nodgCk3fQWOg-kEHRXBJmuEBP3EZWOtaOQBmSFWhrnjSbRKgRjStH6pwApw07FEiOcEuuZ7JpS0d7pPB89V7YWcJO7IkwaNTGfI6kccemutHX1tJbD9Yl3Av-od0vVCfqr3tIt82JLMulMWTvcSMW5fxIDmTwqqXvd3ytYoin41lB7', 'width': 3468}], 'place_id': 'ChIJIeWu482e4jARYymvLJqTQ58', 'plus_code': {'compound_code': 'PGWM+FV Bangkok', 'global_code': '7P52PGWM+FV'}, 'types': ['shopping_mall', 'department_store', 'store', 'point_of_interest', 'establishment']}], 'status': 'OK'}
        return response_data
