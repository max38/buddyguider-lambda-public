import pytest

from src.infrastructure.repositories.googleapi.place import GooglePlaceAPIRepository


def test_get_place_information():
    repository = GooglePlaceAPIRepository()
    response = repository.find_place_from_text('Gardens by the Bay')
    print(response)
    