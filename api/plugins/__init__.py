import inspect

from api.db import JsonDB
from api.exeptions import APIError
from bottle import HTTPError, PluginError, app


class JsonDBPlugin(object):
    name = "jsondb"
    api = 2

    def __init__(self, location: str, keywork="jsondb"):
        self.location = location
        self.keyword = keywork

    def setup(self, app: app):
        for other in app.plugins:
            if not isinstance(other, JsonDBPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another jsondb plugin with "
                                  "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        conf = context.config.get("jsondb") or {}
        location = conf.get("location", self.location)
        keyword = conf.get("keyword", self.keyword)
        args = inspect.getfullargspec(context.callback)[0]

        if self.keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the database
            try:
                jsondb = JsonDB(location)
                kwargs[keyword] = jsondb
            except Exception as e:
                raise HTTPError(500, "Database Error", e)
            return callback(*args, **kwargs)

        return wrapper


class ExceptionPlugin(object):
    name = "exepction"
    api = 2

    def apply(self, callback, context):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except APIError as api_error:
                return api_error.__dict__
        return wrapper


__all__ = ["JsonDBPlugin", "ExceptionPlugin"]
