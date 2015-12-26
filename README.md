Flask Tread
===========

Flask Tread provides Flask route input and output validation, authentication and transformation. Validation and transformation is performed on the url parameters and the input and output json. Authentication is provided by creating and verifying the `token` key.

Instructions
============

Import the desired `flask_tread` functions and classes, then call `init_tread_app(app, login_key)` where `app` is the flask app and `login_key` is a unique string used for authentication.

There are two main routes, `@route` and `@auth_route`. `@auth_route` requires the client to provide a token previously generated using `create_token` for authentication. Routes can take the parameters: `path`, `command`, `params`, `takes`, and `sends`. The parameters `path` and `command` are the url path and json `command` key combo needed to trigger the route.

The parameter `takes` is a dict containing verification or transformation functions. These are run on the json sent to the api. If verification fails, an error sent back to the client. Transformation is performed on each value provided to the api from the client and placed in `flask.g.json_data`. Similar to a verification and transformation, the authentication from`route_auth` populates `flask.g.user_id` for the user id of the `token` key provided. A list of all possible values for input keys to use for verification and transformation are provided below in Doc.

The `params` parameter works similarly to `takes`, but operates on url parameters. The `sends` parameter also works similarly to `takes`, but operates on the output of the api.

For example, `hash_to_id` and `id_to_hash` are useful transformers for converting between database ids and user facing ids. The following route could be used in an api for finding the next user in a queue: 

``` py
@route('/api/user', command='getNextInLine', takes={ 
    'currentUserHash': hash_to_id 
}, sends={ 
    'nextUserHash': id_to_hash 
})
```

The app would then return a database id instead of the client facing hash id for the `nextUserHash` key and the transformation `hash_to_id` would convert it.

Doc
===

- Routes
    - `@route`
        - Standard route
    - `@auth_route`
        - Authenticated route
        - Token created by `create_token`
- Params
    - `params`
        - URL parameters i.e. `/api/object/<object_id>`
    - `takes`
        - json parameters route takes
    - `sends`
        - json parameters route send
- Each of the params takes an object with String keys containing some of the following values:
    - `None`
        - Key required to be present, but can be anything
    - type or class
        - Value accepted for this key must be of this type
    - `{}`
        - Key contains object with these string keys (similar to top level)
    - `[]`
        - This is expected to contain a single expected value, can be object
            which means all values in list must conform to object
    - function
        - Function must return: `(ERROR_KEYWORD, { ERROR_KEYWORD: '<error message>' })`
            - If there is an error in validation, this is returned immediately
        - Or: `TRANSFORM_KEYWORD, <new value>`
            - To transform this object to its new value
        - Or: `None, {}`
            - For no change
    - `id_to_hash`
        - transform function for id to hash
    - `hash_to_id`
        - transform function for hash to id
    - `Optional`
        - used as `Optional(<validator value/transformer>)` for `Optional`
    - `MultiType`
        - Used as `MultiType([type, type, ...])` if one of many types can be accepted
    - `ignored`
        - Indicates key can be present, but will be ignored

Examples
========

View [views.py](/examples/blog/app/mainapp/views.py) for examples of Flask Tread routes.
