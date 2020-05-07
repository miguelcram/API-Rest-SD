from api.plugins import ExceptionPlugin, JsonDBPlugin
from api.routes import *  # noqa: F401, F403
from bottle import hook, install, response, run


@hook("after_request")
def default_headers():
    response.headers["Content-Type"] = "application/json"


install(JsonDBPlugin("./data/db.json"))
install(ExceptionPlugin())

run(host='localhost', port=8080, debug=True)
