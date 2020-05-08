from api.db import JsonDB
from api.exeptions import NotFound
from api.model.room import Room
from api.utils import str2bool
from bottle import delete, get, post, put, request, response


@get("/rooms")
def list_room(jsondb: JsonDB):
    if "booked" in request.query:
        res = jsondb.find_document_by(
            "rooms",
            lambda room: room['booked'] == str2bool(request.query.booked)
        )
        print(res)
        return dict(data=res)
    return dict(data=jsondb.documents("rooms"))


@get("/rooms/<id>")
def get_room(id: str, jsondb: JsonDB):
    try:
        return jsondb.find_document_by_id("rooms", id)
    except KeyError:
        raise NotFound


@post("/rooms")
def create_room(jsondb: JsonDB):
    room = Room(**request.json)
    id = jsondb.insert_document("rooms", room)
    response.status = 201

    return {'id': id}


@put("/rooms/<id>")
def update_room(id: str, jsondb: JsonDB):
    try:
        data = request.json
        Room.validate_update(**data)
        updated = jsondb.update_document_by("rooms", id, data)
        response.status = 200
        return updated
    except KeyError:
        raise NotFound


@delete("/rooms/<id>")
def delete_room(id: str, jsondb: JsonDB):
    try:
        jsondb.delete_document_by("rooms", id)
        response.status = 204
    except KeyError:
        raise NotFound
