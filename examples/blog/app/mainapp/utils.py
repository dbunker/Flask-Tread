import uuid
import datetime

def get_time():
    return datetime.datetime.utcnow()

def random_id():
    return str(uuid.uuid4())

def pretty_print(input_dict):
    print json.dumps(input_dict, sort_keys=True, indent=4, separators=(',', ': '))
