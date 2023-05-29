import pytest

from src.infrastructure.repositories.database.dynamo.place import PlaceDynamoDBRepository


def test_get_place_by_slug():
    place_slug = 'singapore-centralregion-merlionpark'
    repository = PlaceDynamoDBRepository()
    response = repository.get_place_by_slug(place_slug)
    print(response)
