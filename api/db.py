import json
import os
from typing import Any, Callable, List


class JsonDB(object):
    key_string_error = TypeError('Key/name must be a string!')

    def __init__(self, location: str, auto_dump=True):
        '''Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update.
        '''
        self.load(location, auto_dump)

    def load(self, location: str, auto_dump: bool) -> True:
        '''Loads, reloads or changes the path to the db file'''
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True

    def dump(self) -> True:
        '''Force dump memory db to file'''
        with open(self.loco, 'wt') as file:
            json.dump(self.db, file)
        return True

    def _loaddb(self) -> None:
        '''Load or reload the json info from the file'''
        try:
            with open(self.loco, 'rt') as file:
                self.db = json.load(file)
        except ValueError:
            # Error raised because file is empty
            if os.stat(self.loco).st_size == 0:
                self.db = {}
            else:
                raise  # File is not empty, avoid overwriting it

    def _autodumpdb(self) -> None:
        '''Write/save the json dump into the file if auto_dump is enabled'''
        if self.auto_dump:
            self.dump()

    def set(self, key: str, value: Any) -> True:
        '''Set the str value of a key'''
        if isinstance(key, str):
            self.db[key] = value
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def get(self, key) -> Any:
        '''Get the value of a key'''
        try:
            return self.db[key]
        except KeyError:
            return None

    def insert_document(self, collection: str, document: Any) -> int:
        ''' Insert Document into collection an returns an id'''
        document = document.__dict__
        if collection not in self.db:
            self.db[collection] = {}
            self.db[collection + '_id'] = 1
        self.db[collection + '_id'] += 1
        document['id'] = self.db[collection + '_id']
        self.db[collection][document['id']] = document
        if self.auto_dump:
            self._autodumpdb()
        return document['id']

    def documents(self, collection: str) -> List[Any]:
        if collection in self.db:
            return list(self.db[collection].values())
        return []

    def find_document_by_id(self, collection: str, id: str) -> Any:
        return self.db[collection][id]

    def find_document_by(
            self, collection: str, func: Callable[[Any], Any]) -> List[Any]:
        return list(filter(func, self.db[collection].values()))

    def update_document_by(self, collection, id, document) -> Any:
        self.db[collection][id].update(document)
        if self.auto_dump:
            self._autodumpdb()
        return self.db[collection][id]

    def delete_document_by(self, collection, id) -> None:
        del self.db[collection][id]
        if self.auto_dump:
            self._autodumpdb()
