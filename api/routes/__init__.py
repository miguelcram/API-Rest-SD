from typing import Any, List

from api.db import JsonDB
from api.exeptions import NotFound
from bottle import delete, get, post, put, request, response
from api.model.room import Room


def find_room_by_id(id: str, rooms: List[Any]):
    room = next(filter(lambda room: room["id"] == int(id), rooms), None)
    if room is None:
        raise NotFound
    return room


@get("/rooms")
def list_room(jsondb: JsonDB):
    return dict(data=jsondb.lgetall("rooms"))


@get("/rooms/<id>")
def get_room(id: str, jsondb: JsonDB):
    return find_room_by_id(id, jsondb.lgetall("rooms"))


@post("/rooms")
def create_room(jsondb: JsonDB):
    data = Room(**request.json)
    id = jsondb.ladd("rooms", data.__dict__)
    response.status = 201

    return {'id': id}


@put("/rooms/<id>")
def update_room(id: str, jsondb: JsonDB):
    # data = request.json
    rooms = jsondb.lgetall("rooms")
    room = next(filter(lambda room: room["id"] == int(id), rooms), None)
    if room is None:
        raise NotFound
    return room


@delete("/rooms/<id>")
def delete_room(id: str, jsondb: JsonDB):
    rooms = jsondb.lgetall("rooms")
    room = find_room_by_id(id, rooms)
    return room


@get("/rooms/state")
def empty_rooms():
    pass


__all__ = ["list_room", "get_room",
           "create_room", "update_room", "empty_rooms"]
