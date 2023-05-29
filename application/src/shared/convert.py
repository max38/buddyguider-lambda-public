import re
import json
from decimal import Decimal
from datetime import datetime


def str_iso_datetime_to_datetime(str_iso_datetime):
    return datetime.strptime(str_iso_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")


def datetime_to_str_iso_datetime(datetime_obj):
    if not datetime_obj:
        return None
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def str_to_float_regex(str_data):
    float_list = re.findall(r"\d+\.\d+|\d+", str_data)
    if len(float_list) == 0:
        return 0
    return float(float_list[0])



class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        if isinstance(obj, Decimal):
            return float(obj)
        
        if isinstance(obj, bytes):
            return obj.decode('utf-8')

        return json.JSONEncoder.default(self, obj)
    
def dict_to_json(dict_data):
    return json.dumps(dict_data, cls=CustomEncoder)


def float_to_decimal(float_data):
    return Decimal(str(float_data))
