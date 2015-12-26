import requests
import json
import mainapp, flask, os

def pretty_print(input_dict, text=None):
    print json.dumps(input_dict, sort_keys=True, indent=4, separators=(',', ': '))
    if text != None:
        print text

################################
# hit the database

def db_dev_config():
    mainapp.configure('config.DevConfig')

def db_test_config():
    mainapp.configure('config.TestConfig')

def db_delete_all():
    engine = mainapp.db.engine
    meta = mainapp.db.metadata

    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())

################################
# fully hit the api

def make_request(path, data):
    r = requests.post('http://localhost:5005/api' + path, data=json.dumps(data))
    try:
        answer_json = r.json()
    except ValueError:
        print 'JSON Not Returned'
        print 'path: ' + path
        print 'data: ' + str(data)
        print 'text: ' + r.text
        print 'status: ' + str(r.status_code)
        exit()

    return answer_json

def signup_call():
    data = {
        'command': 'signup',
        'username': 'test_user',
        'email': 'test_user@test_user.com',
        'password': 'password'
    }
    return make_request('/user', data)

def login_call():
    data = {
        'command': 'login',
        'usernameEmail': 'test_user',
        'password': 'password'
    }
    return make_request('/user', data)

def check_token(token):
    data = {
        'command': 'checkToken',
        'token': token
    }
    return make_request('/user', data)

def create_comment(token, text):
    data = {
        'command': 'create',
        'token': token,
        'text': text
    }
    return make_request('/comment', data)

def get_comments(token):
    data = {
        'command': 'get',
        'token': token
    }
    return make_request('/comment', data)

def get_single_comment(token, comment_hash):
    data = {
        'command': 'get',
        'token': token
    }
    return make_request('/comment/' + comment_hash, data)

def bad_token():
    data = {
        'token': 'blah'
    }
    return make_request('/comment', data)

def bad_command(token):
    data = {
        'command': 'blah',
        'token': token
    }
    return make_request('/comment', data)

def test():

    db_test_config()
    db_delete_all()

    resp = signup_call()
    pretty_print(resp, 'Signup')
    assert resp['username'] == 'test_user'

    resp = login_call()
    pretty_print(resp, 'Login')
    token = resp['token']

    resp = check_token(token)
    pretty_print(resp, 'Check Token')

    resp = create_comment(token, 'new comment')
    pretty_print(resp, 'Create Comment')
    comment_hash = resp['commentId']

    resp = get_comments(token)
    pretty_print(resp, 'Get Comments')
    assert resp['comments'][0]['text'] == 'new comment'

    resp = get_single_comment(token, comment_hash)
    pretty_print(resp, 'Get Single Comment')

    resp = bad_token()
    pretty_print(resp, 'Bad Token')
    assert 'error' in resp

    resp = bad_command(token)
    pretty_print(resp, 'Bad Command')
    assert 'error' in resp

    print 'Tests Completed Successfully'

if __name__ == '__main__':
    test()
