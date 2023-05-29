from abc import ABC, abstractmethod


class MessagingQueueRepository(ABC):
    
    @abstractmethod
    def publish(self, message: dict):
        pass

    # @abstractmethod
    # def subscribe(self, callback):
    #     pass
