import flask
from flask import jsonify
from flask import Response, request

import random
import time
import copy
import types
import uuid

from functools import wraps
from passlib.hash import sha256_crypt
from hashids import Hashids
hashids = Hashids(min_length=11)

##################
# Decorators

COMMAND_KEYWORD = 'command'
TOKEN_KEYWORD = 'token'
ERROR_KEYWORD = 'error'
TRANSFORM_KEYWORD = 'transform'

def init_tread_app(app, login_key):

    global APP
    global LOGIN_KEY

    APP = app
    LOGIN_KEY = login_key

def random_id():
    return str(uuid.uuid4())

class DecoratorError(Exception):
    def __init__(self, value):
        self.value = value

def id_to_hash(id):
    if id == None:
        return ERROR_KEYWORD, { ERROR_KEYWORD: 'id cannot be null in id to hash' }

    hash_result = hashids.encode(id, 0)
    if hash_result == '':
        return ERROR_KEYWORD, { ERROR_KEYWORD: 'id cannot be hashed' }

    return TRANSFORM_KEYWORD, hash_result

def hash_to_id(hash):
    if hash == None:
        return ERROR_KEYWORD, { ERROR_KEYWORD: 'hash cannot be null in hash to id' }

    decoded_hash = hashids.decode(hash)
    if len(decoded_hash) < 2:
        return ERROR_KEYWORD, { ERROR_KEYWORD: 'user not authorized for request' }
    return TRANSFORM_KEYWORD, decoded_hash[0]

def create_token(user_id):
    status, user_hash = id_to_hash(user_id)
    unixtime = str(time.time())
    key_token = unixtime + user_hash + LOGIN_KEY
    return unixtime + '-' + user_hash + '-' + sha256_crypt.encrypt(key_token)

def verify_token(token):

    split_token = token.split('-', 2)
    if len(split_token) != 3:
        return False

    try:
        unixtime = float(split_token[0])
    except ValueError:
        return False

    if time.time() < unixtime or time.time() - 60*60*24 > unixtime:
        return False

    user_hash = split_token[1]
    token_hash = split_token[2]

    to_check = str(unixtime) + user_hash + LOGIN_KEY
    return sha256_crypt.verify(to_check, token_hash)

def get_user_hash(token):
    return token.split('-', 2)[1]

function_commands = {}

# to be callable
# instance.__call__ = lambda value: value.upper()
class Optional:

    def __init__(self, param, default_value=None):
        self.param = param
        self.default_value = default_value

    def get_default(self):
        return self.default_value

class MultiType:

    def __init__(self, *args):
        self.multi_types = args

    def is_instance(self, to_check):
        for multi_type in self.multi_types:
            if isinstance(to_check, multi_type):
                return True
        return False

    def get_multi_types(self):
        return self.multi_types

class Ignored:
    pass

ignored = Ignored()

def transform_input(expected, to_check):

    if isinstance(expected, dict):

        if not isinstance(to_check, dict):
            return ERROR_KEYWORD, { ERROR_KEYWORD: 'key not of correct type: dict' }

        for key, new_expected in expected.iteritems():

            if isinstance(new_expected, Ignored):
                if key in to_check:
                    del to_check[key]
                continue

            if isinstance(new_expected, Optional):
                # if type Optional, value None is added when not present
                if key not in to_check or to_check[key] == None:
                    to_check[key] = new_expected.get_default()
                    continue

            if key not in to_check:
                return ERROR_KEYWORD, { ERROR_KEYWORD: 'missing key', 'key': str(key) }

            status, response = transform_input(new_expected, to_check[key])
            if status == TRANSFORM_KEYWORD:
                to_check[key] = response

            elif status == ERROR_KEYWORD:
                if 'key' in response:
                    response['key'] = key + '.' + response['key']
                else:
                    response['key'] = key
                return status, response

        to_check_keys = to_check.keys()
        expected_keys = expected.keys()

        for key in to_check_keys:
            if key not in expected_keys:
                print expected_keys
                return ERROR_KEYWORD, { ERROR_KEYWORD: 'unexpected extra key', 'key': str(key) }

        return None, {}

    elif isinstance(expected, Optional):
        status, response = transform_input(expected.param, to_check)
        return status, response

    elif expected == None:
        return None, {}

    elif isinstance(expected, list):

        if not isinstance(to_check, list):
            return ERROR_KEYWORD, { ERROR_KEYWORD: 'key not of correct type: list' }

        new_expected = expected[0]

        for i in range(0, len(to_check)):
            status, response = transform_input(new_expected, to_check[i])
            if status != None:
                return status, response

        return None, {}

    elif isinstance(expected, type) or isinstance(expected, types.ClassType):

        if not isinstance(to_check, expected):

            if expected == unicode and type(to_check) == str:
                return TRANSFORM_KEYWORD, unicode(to_check, "utf-8")

            else:
                return ERROR_KEYWORD, {
                    ERROR_KEYWORD: 'key not of correct type: ' +  str(expected)
                }
        return None, {}

    elif isinstance(expected, MultiType):

        # expected.is_instance checks if to_check is of correct type
        if not expected.is_instance(to_check):
            return ERROR_KEYWORD, {
                ERROR_KEYWORD: 'key not of correct type: ' + str(expected.get_multi_types())
            }
        return None, {}

    elif callable(expected):
        get_transform = expected(to_check)
        status, response = get_transform
        return status, response

    else:
        return ERROR_KEYWORD, {
            ERROR_KEYWORD: 'do not recognize type: ' + str(exptected)
        }

def route(path, command, auth=False, params={}, takes={}, sends={}):
    def route_decorator(function):

        @wraps(function)
        def function_wrapper(*args, **kwargs):

            # copy route input to mutate
            json_data = copy.deepcopy(flask.g.json_data)
            path_params = copy.deepcopy(flask.g.path_params)

            # auth
            if auth:
                if TOKEN_KEYWORD not in json_data:
                    return { ERROR_KEYWORD: 'token not found' }

            if TOKEN_KEYWORD in json_data:
                token = json_data[TOKEN_KEYWORD]
                del json_data[TOKEN_KEYWORD]

                if not verify_token(token):
                    return { ERROR_KEYWORD: 'could not authenticate' }

                userhash = get_user_hash(token)
                status, user_id = hash_to_id(userhash)
                if status == ERROR_KEYWORD:
                    response = user_id
                    return response

                flask.g.user_id = user_id
                flask.g.user_hash_id = userhash

            # params
            status, response = transform_input(params, kwargs)
            if status != None:
                return response

            # takes
            status, response = transform_input(takes, json_data)
            if status != None:
                return response

            flask.g.json_data = json_data
            flask.g.path_params = path_params

            final_response = function(*args, **kwargs)

            # sends
            if ERROR_KEYWORD in final_response:
                return final_response
            else:
                status, response = transform_input(sends, final_response)

                # for debugging
                if status != None:
                    response['errorType'] = 'internal error'
                    return response

            return final_response

        if path not in function_commands:

            def check_commands(*args, **kwargs):

                json_data = request.get_json(force=True, silent=True)
                if json_data == None:
                    return { ERROR_KEYWORD: 'no json data' }

                flask.g.json_data = json_data
                flask.g.path_params = kwargs

                # command
                if COMMAND_KEYWORD not in json_data:
                    return { ERROR_KEYWORD: 'no command' }

                command = json_data[COMMAND_KEYWORD]
                del json_data[COMMAND_KEYWORD]

                if command not in function_commands[path]:
                    return { ERROR_KEYWORD: 'invalid command' }

                return function_commands[path][command](*args, **kwargs)

            @wraps(check_commands)
            def check_commands_json_wrapper(*args, **kwargs):
                response = check_commands(*args, **kwargs)
                status = 200
                if ERROR_KEYWORD in response:
                    status = 400
                return jsonify(response), status

            APP.add_url_rule(path, random_id(), check_commands_json_wrapper, methods=['POST'])
            function_commands[path] = {}

        if command in function_commands[path]:
            error_message = 'Error: command (' + command + ') already exists for path (' + path + ')'
            print error_message
            raise DecoratorError(error_message)

        function_commands[path][command] = function_wrapper

        return function_wrapper

    return route_decorator

def auth_route(path, command, auth=True, params={}, takes={}, sends={}):
    return route(path, command, auth, params, takes, sends)

def print_queries():
    print '------'
    for query in flask.ext.sqlalchemy.get_debug_queries():
        print query
    print '------'
