from abc import ABC, abstractmethod

from src.domain.entities.place import PlaceEntity


class PlaceRepository(ABC):
    
    @abstractmethod
    def create_place(self, place: PlaceEntity) -> PlaceEntity:
        pass

    @abstractmethod
    def get_place_by_id(self, place_id: str) -> PlaceEntity:
        pass

    @abstractmethod
    def get_place_by_slug(self, place_slug: str) -> PlaceEntity:
        pass

    @abstractmethod
    def update_place_by_id(self, place_id: str, place: PlaceEntity) -> PlaceEntity:
        pass

    @abstractmethod
    def update_or_create_place_by_slug(self, place_slug: str, place: PlaceEntity) -> PlaceEntity:
        pass
