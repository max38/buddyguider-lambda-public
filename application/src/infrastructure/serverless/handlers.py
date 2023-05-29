from src.interface.adapter.serverless.sqs import UserPlanningRequestSqsAdapter
from src.interface.adapter.serverless.api_gateway import UserPlanningRequestApiAdapter, GetSuggestionResultApiAdapter, GetPlaceInformationApiAdapter


def suggestion_sqs_handler(event, context):
    return UserPlanningRequestSqsAdapter(event, context).execute()


def get_suggestion_api_handler(event, context):
    return GetSuggestionResultApiAdapter(event, context).execute()


def request_suggestion_api_handler(event, context):
    return UserPlanningRequestApiAdapter(event, context).execute()


def get_place_information_api_handler(event, context):
    return GetPlaceInformationApiAdapter(event, context).execute()
