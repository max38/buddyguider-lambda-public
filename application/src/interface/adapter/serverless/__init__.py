import json

from src.domain.adapters.base import Adapter


class ServerLessAdapter(Adapter):

    def __init__(self, event, context) -> None:
        self.event = event
        self.context = context
        self.body = self._get_body_data_from_event()

    def _get_request_id_from_context(self):
        return self.context.aws_request_id
    
    def _get_body_data_from_event(self):
        if 'body' in self.event and self.event['body'] is not None:        
            return json.loads(self.event['body'])
        return None
