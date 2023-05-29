from src.domain.entities.place import PlaceEntity

from .base import TripAdvisorRepository


class TripAdvisorLocationAPIRepository(TripAdvisorRepository):
    
    def get_location_detail(self, location_id: str):
        url = f"v1/location/{location_id}/details"
        params = {
            'language': 'en',
            'currency': 'USD'
        }
        response = self.request_get(url, params=params)
#         {
#   "location_id": "190545",
#   "name": "Berliner Dom",
#   "web_url": "https://www.tripadvisor.com/Attraction_Review-g187323-d190545-Reviews-Berliner_Dom-Berlin.html?m=66827",
#   "address_obj": {
#     "street1": "Am Lustgarten",
#     "city": "Berlin",
#     "country": "Germany",
#     "postalcode": "10178",
#     "address_string": "Am Lustgarten, 10178 Berlin Germany"
#   },
#   "ancestors": [
#     {
#       "level": "City",
#       "name": "Berlin",
#       "location_id": "187323"
#     },
#     {
#       "level": "Country",
#       "name": "Germany",
#       "location_id": "187275"
#     }
#   ],
#   "latitude": "52.51915",
#   "longitude": "13.401108",
#   "timezone": "Europe/Berlin",
#   "email": "info@berlinerdom.de",
#   "phone": "+49 30 20269136",
#   "website": "http://www.berlinerdom.de",
#   "write_review": "https://www.tripadvisor.com/UserReview-g187323-d190545-Berliner_Dom-Berlin.html?m=66827",
#   "ranking_data": {
#     "geo_location_id": "187323",
#     "ranking_string": "#33 of 1,214 things to do in Berlin",
#     "geo_location_name": "Berlin",
#     "ranking_out_of": "1214",
#     "ranking": "33"
#   },
#   "rating": "4.5",
#   "rating_image_url": "https://www.tripadvisor.com/img/cdsi/img2/ratings/traveler/4.5-66827-5.svg",
#   "num_reviews": "10605",
#   "review_rating_count": {
#     "1": "105",
#     "2": "150",
#     "3": "879",
#     "4": "3303",
#     "5": "6168"
#   },
#   "photo_count": "11453",
#   "see_all_photos": "https://www.tripadvisor.com/Attraction_Review-g187323-d190545-m66827-Reviews-Berliner_Dom-Berlin.html#photos",
#   "hours": {
#     "periods": [
#       {
#         "open": {
#           "day": 1,
#           "time": "1000"
#         },
#         "close": {
#           "day": 1,
#           "time": "1800"
#         }
#       },
#       {
#         "open": {
#           "day": 2,
#           "time": "1000"
#         },
#         "close": {
#           "day": 2,
#           "time": "1800"
#         }
#       },
#       {
#         "open": {
#           "day": 3,
#           "time": "1000"
#         },
#         "close": {
#           "day": 3,
#           "time": "1800"
#         }
#       },
#       {
#         "open": {
#           "day": 4,
#           "time": "1000"
#         },
#         "close": {
#           "day": 4,
#           "time": "1800"
#         }
#       },
#       {
#         "open": {
#           "day": 5,
#           "time": "1000"
#         },
#         "close": {
#           "day": 5,
#           "time": "1800"
#         }
#       },
#       {
#         "open": {
#           "day": 6,
#           "time": "1000"
#         },
#         "close": {
#           "day": 6,
#           "time": "1700"
#         }
#       },
#       {
#         "open": {
#           "day": 7,
#           "time": "1200"
#         },
#         "close": {
#           "day": 7,
#           "time": "1700"
#         }
#       }
#     ],
#     "weekday_text": [
#       "Monday: 10:00 - 18:00",
#       "Tuesday: 10:00 - 18:00",
#       "Wednesday: 10:00 - 18:00",
#       "Thursday: 10:00 - 18:00",
#       "Friday: 10:00 - 18:00",
#       "Saturday: 10:00 - 17:00",
#       "Sunday: 12:00 - 17:00"
#     ]
#   },
#   "category": {
#     "name": "attraction",
#     "localized_name": "Attraction"
#   },
#   "subcategory": [
#     {
#       "name": "landmarks",
#       "localized_name": "Sights & Landmarks"
#     },
#     {
#       "name": "attractions",
#       "localized_name": "Attractions"
#     }
#   ],
#   "groups": [
#     {
#       "name": "Sights & Landmarks",
#       "localized_name": "Sights & Landmarks",
#       "categories": [
#         {
#           "name": "Architectural Buildings",
#           "localized_name": "Architectural Buildings"
#         },
#         {
#           "name": "Churches & Cathedrals",
#           "localized_name": "Churches & Cathedrals"
#         }
#       ]
#     }
#   ],
#   "trip_types": [
#     {
#       "name": "business",
#       "localized_name": "Business",
#       "value": "239"
#     },
#     {
#       "name": "couples",
#       "localized_name": "Couples",
#       "value": "3843"
#     },
#     {
#       "name": "solo",
#       "localized_name": "Solo travel",
#       "value": "1100"
#     },
#     {
#       "name": "family",
#       "localized_name": "Family",
#       "value": "1709"
#     },
#     {
#       "name": "friends",
#       "localized_name": "Friends getaway",
#       "value": "2078"
#     }
#   ],
#   "awards": [
#     {
#       "award_type": "Travelers Choice",
#       "year": "2022",
#       "images": {
#         "small": "https://www.tripadvisor.com/img/cdsi/img2/awards/CERTIFICATE_OF_EXCELLENCE_v2_small-66827-5.jpg",
#         "large": "https://www.tripadvisor.com/img/cdsi/img2/awards/CERTIFICATE_OF_EXCELLENCE_2022_en_US_large-66827-5.jpg"
#       },
#       "categories": [],
#       "display_name": "Travelers Choice 2022"
#     }
#   ]
# }

        return response
    
    def get_location_photos(self, location_id: str):
        url = f"v1/location/{location_id}/photos"
        params = {
            'language': 'en',
        }
        response = self.request_get(url, params=params)
#         {
#   "data": [
#     {
#       "id": 237786196,
#       "is_blessed": false,
#       "caption": "",
#       "published_date": "2017-01-16T19:40:39.511Z",
#       "images": {
#         "thumbnail": {
#           "height": 50,
#           "width": 50,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-t/0e/2c/54/54/photo0jpg.jpg"
#         },
#         "small": {
#           "height": 150,
#           "width": 150,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-l/0e/2c/54/54/photo0jpg.jpg"
#         },
#         "medium": {
#           "height": 205,
#           "width": 210,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-f/0e/2c/54/54/photo0jpg.jpg"
#         },
#         "large": {
#           "height": 450,
#           "width": 460,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-s/0e/2c/54/54/photo0jpg.jpg"
#         },
#         "original": {
#           "height": 626,
#           "width": 640,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-o/0e/2c/54/54/photo0jpg.jpg"
#         }
#       },
#       "album": "Other",
#       "source": {
#         "name": "Traveler",
#         "localized_name": "Traveler"
#       },
#       "user": {
#         "username": "_N6475AY"
#       }
#     },
#     {
#       "id": 313156509,
#       "is_blessed": false,
#       "caption": "Foto Bednorz",
#       "published_date": "2018-04-17T09:13:36.368Z",
#       "images": {
#         "thumbnail": {
#           "height": 50,
#           "width": 50,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-t/12/aa/63/9d/foto-bednorz.jpg"
#         },
#         "small": {
#           "height": 150,
#           "width": 150,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-l/12/aa/63/9d/foto-bednorz.jpg"
#         },
#         "medium": {
#           "height": 180,
#           "width": 250,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-f/12/aa/63/9d/foto-bednorz.jpg"
#         },
#         "large": {
#           "height": 396,
#           "width": 550,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-s/12/aa/63/9d/foto-bednorz.jpg"
#         },
#         "original": {
#           "height": 1440,
#           "width": 2000,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-o/12/aa/63/9d/foto-bednorz.jpg"
#         }
#       },
#       "album": "Other",
#       "source": {
#         "name": "Management",
#         "localized_name": "Management"
#       },
#       "user": {
#         "username": "Management"
#       }
#     },
#     {
#       "id": 313472994,
#       "is_blessed": false,
#       "caption": "Kuppel mit Altarkreuz",
#       "published_date": "2018-04-19T09:18:27.652Z",
#       "images": {
#         "thumbnail": {
#           "height": 50,
#           "width": 50,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-t/12/af/37/e2/kuppel-mit-altarkreuz.jpg"
#         },
#         "medium": {
#           "height": 200,
#           "width": 180,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-i/12/af/37/e2/kuppel-mit-altarkreuz.jpg"
#         },
#         "small": {
#           "height": 150,
#           "width": 150,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-l/12/af/37/e2/kuppel-mit-altarkreuz.jpg"
#         },
#         "large": {
#           "height": 450,
#           "width": 298,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-s/12/af/37/e2/kuppel-mit-altarkreuz.jpg"
#         },
#         "original": {
#           "height": 1024,
#           "width": 678,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-o/12/af/37/e2/kuppel-mit-altarkreuz.jpg"
#         }
#       },
#       "album": "Other",
#       "source": {
#         "name": "Management",
#         "localized_name": "Management"
#       },
#       "user": {
#         "username": "Management"
#       }
#     },
#     {
#       "id": 313472990,
#       "is_blessed": false,
#       "caption": "Altarraum. Foto: Katarina Dorn",
#       "published_date": "2018-04-19T09:18:25.289Z",
#       "images": {
#         "thumbnail": {
#           "height": 50,
#           "width": 50,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-t/12/af/37/de/altarraum-foto-katarina.jpg"
#         },
#         "small": {
#           "height": 150,
#           "width": 150,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-l/12/af/37/de/altarraum-foto-katarina.jpg"
#         },
#         "medium": {
#           "height": 200,
#           "width": 180,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-i/12/af/37/de/altarraum-foto-katarina.jpg"
#         },
#         "large": {
#           "height": 450,
#           "width": 344,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-s/12/af/37/de/altarraum-foto-katarina.jpg"
#         },
#         "original": {
#           "height": 617,
#           "width": 472,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-o/12/af/37/de/altarraum-foto-katarina.jpg"
#         }
#       },
#       "album": "Other",
#       "source": {
#         "name": "Management",
#         "localized_name": "Management"
#       },
#       "user": {
#         "username": "Management"
#       }
#     },
#     {
#       "id": 313472988,
#       "is_blessed": false,
#       "caption": "Sauer-Orgel. Foto: Maren Glockner",
#       "published_date": "2018-04-19T09:18:23.286Z",
#       "images": {
#         "thumbnail": {
#           "height": 50,
#           "width": 50,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-t/12/af/37/dc/sauer-orgel-foto-maren.jpg"
#         },
#         "medium": {
#           "height": 200,
#           "width": 180,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-i/12/af/37/dc/sauer-orgel-foto-maren.jpg"
#         },
#         "small": {
#           "height": 150,
#           "width": 150,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-l/12/af/37/dc/sauer-orgel-foto-maren.jpg"
#         },
#         "large": {
#           "height": 450,
#           "width": 298,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-s/12/af/37/dc/sauer-orgel-foto-maren.jpg"
#         },
#         "original": {
#           "height": 1500,
#           "width": 994,
#           "url": "https://media-cdn.tripadvisor.com/media/photo-o/12/af/37/dc/sauer-orgel-foto-maren.jpg"
#         }
#       },
#       "album": "Other",
#       "source": {
#         "name": "Management",
#         "localized_name": "Management"
#       },
#       "user": {
#         "username": "Management"
#       }
#     }
#   ]
# }
        return response
    
    def location_search_by_place(self, place: PlaceEntity):
        url = "v1/location/search"
        params = {
            'searchQuery': place.name,
            'latLong': f'{place.location_lat},{place.location_long}',
            'language': 'en',
        }
        response = self.request_get(url, params=params)
        
        if response is None:
            return None
        elif 'data' in response and len(response['data']) > 0:
            return response['data']

#         {
#   "data": [
#     
    # {
    #   "location_id": "265635",
    #   "name": "Musee de l’Orangerie",
    #   "distance": "0.009019033954921657",
    #   "bearing": "southeast",
    #   "address_obj": {
    #     "street1": "Jardin des Tuileries - Cote Seine",
    #     "city": "Paris",
    #     "country": "France",
    #     "postalcode": "75058",
    #     "address_string": "Jardin des Tuileries - Cote Seine, 75058 Paris France"
    #   }
    # },
#     {
#       "location_id": "196239",
#       "name": "Memorial of the Berlin Wall",
#       "address_obj": {
#         "street1": "Bernauer Strasse 111",
#         "city": "Berlin",
#         "country": "Germany",
#         "postalcode": "13355",
#         "address_string": "Bernauer Strasse 111, 13355 Berlin Germany"
#       }
#     }
#   ]
# }
        return response