import json

from api.plugins import ExceptionPlugin, JsonDBPlugin
from api.routes import *  # noqa: F401, F403
from bottle import error, hook, install, response, run


@hook("after_request")
def default_headers():
    response.content_type = 'application/json'


@error(500)
@error(405)
@error(404)
def error_codes(error):
    response.content_type = 'application/json'
    return json.dumps({
        'message': error._status_line,
        'status': error._status_code
    })


install(JsonDBPlugin("./data/db.json"))
install(ExceptionPlugin())

run(host='localhost', port=8080, debug=True)
