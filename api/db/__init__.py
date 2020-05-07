import json
import os
import signal
import sys
from threading import Thread
from typing import Any, Dict, List, Tuple


class JsonDB(object):
    key_string_error = TypeError('Key/name must be a string!')

    def __init__(self, location: str, auto_dump=True, sig=True):
        '''Creates a database object and loads the data from the location path.
        If the file does not exist it will be created on the first update.
        '''
        self.load(location, auto_dump)
        self.dthread = None
        if sig:
            self.set_sigterm_handler()

    def __getitem__(self, item: str) -> Any:
        '''Syntax sugar for get()'''
        return self.get(item)

    def __setitem__(self, key: str, value: Any) -> bool:
        '''Sytax sugar for set()'''
        return self.set(key, value)

    def __delitem__(self, key: str) -> bool:
        '''Sytax sugar for rem()'''
        return self.rem(key)

    def set_sigterm_handler(self) -> None:
        '''Assigns sigterm_handler for graceful shutdown during dump()'''
        def sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, sigterm_handler)

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
        self.dthread = Thread(
            target=json.dump,
            args=(self.db, open(self.loco, 'wt')))
        self.dthread.start()
        self.dthread.join()
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

    def getall(self) -> List[str]:
        '''Return a list of all keys in db'''
        return self.db.keys()

    def exists(self, key: str) -> bool:
        '''Return True if key exists in db, return False if not'''
        return key in self.db

    def rem(self, key: str) -> bool:
        '''Delete a key'''
        if key not in self.db:
            return False
        del self.db[key]
        self._autodumpdb()
        return True

    def totalkeys(self, name=None) -> int:
        '''Get a total number of keys, lists, and dicts inside the db'''
        if name is None:
            total = len(self.db)
            return total
        else:
            total = len(self.db[name])
            return total

    def append(self, key: str, more: List[Any]) -> True:
        '''Add more to a key's value'''
        tmp = self.db[key]
        self.db[key] = tmp + more
        self._autodumpdb()
        return True

    def lcreate(self, name: str) -> True:
        '''Create a list, name must be str'''
        if isinstance(name, str):
            self.db[name] = []
            self.db[name+"_id"] = 0
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def ladd(self, name: str, value: Any) -> int:
        '''Add a value to a list'''
        if not self.exists(name):
            self.lcreate(name)
        self.db[name+"_id"] += 1
        value["id"] = self.db[name+"_id"]
        self.db[name].append(value)
        self._autodumpdb()
        return self.db[name+"_id"]

    def lextend(self, name: str, seq: List[Any]) -> True:
        '''Extend a list with a sequence'''
        self.db[name].extend(seq)
        self._autodumpdb()
        return True

    def lgetall(self, name: str) -> List[Any]:
        '''Return all values in a list'''
        return self.db[name]

    def lget(self, name: str, pos: int) -> Any:
        '''Return one value in a list'''
        return self.db[name][pos]

    def lrange(self, name: str, start=None, end=None) -> List[Any]:
        '''Return range of values in a list '''
        return self.db[name][start:end]

    def lremlist(self, name: str) -> int:
        '''Remove a list and all of its values'''
        number = len(self.db[name])
        del self.db[name]
        self._autodumpdb()
        return number

    def lremvalue(self,
                  name: str, value: Any, callback=lambda v: lambda x: v == x):
        '''Remove a value from a certain list'''
        initial = self.llen(name)
        self.db[name] = filter(callback(value), self.db[name])
        after = self.llen(name)
        self.db[name+"_id"] = self.db[name+"_id"] + (initial-after)
        self._autodumpdb()
        return True

    def lpop(self, name: str, pos: int) -> Any:
        '''Remove one value in a list'''
        value = self.db[name][pos]
        del self.db[name][pos]
        self._autodumpdb()
        return value

    def llen(self, name: str) -> int:
        '''Returns the length of the list'''
        return len(self.db[name])

    def lappend(self, name: str, pos: int, more: Any) -> True:
        '''Add more to a value in a list'''
        tmp = self.db[name][pos]
        self.db[name][pos] = tmp + more
        self._autodumpdb()
        return True

    def lexists(self, name: str, value: Any) -> bool:
        '''Determine if a value  exists in a list'''
        return value in self.db[name]

    def dcreate(self, name: str) -> True:
        '''Create a dict, name must be str'''
        if isinstance(name, str):
            self.db[name] = {}
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def dadd(self, name: str, pair: Tuple[str, Any]) -> True:
        '''Add a key-value pair to a dict, "pair" is a tuple'''
        self.db[name][pair[0]] = pair[1]
        self._autodumpdb()
        return True

    def dget(self, name: str, key: str) -> Any:
        '''Return the value for a key in a dict'''
        return self.db[name][key]

    def dgetall(self, name: str) -> Dict[str, Any]:
        '''Return all key-value pairs from a dict'''
        return self.db[name]

    def drem(self, name: str) -> True:
        '''Remove a dict and all of its pairs'''
        del self.db[name]
        self._autodumpdb()
        return True

    def dpop(self, name: str, key: str) -> Any:
        '''Remove one key-value pair in a dict'''
        value = self.db[name][key]
        del self.db[name][key]
        self._autodumpdb()
        return value

    def dkeys(self, name: str) -> List[str]:
        '''Return all the keys for a dict'''
        return self.db[name].keys()

    def dvals(self, name: str) -> List[Any]:
        '''Return all the values for a dict'''
        return self.db[name].values()

    def dexists(self, name: str, key: str) -> bool:
        '''Determine if a key exists or not in a dict'''
        return key in self.db[name]

    def dmerge(self, name1: str, name2: str) -> True:
        '''Merge two dicts together into name1'''
        first = self.db[name1]
        second = self.db[name2]
        first.update(second)
        self._autodumpdb()
        return True

    def deldb(self) -> True:
        '''Delete everything from the database'''
        self.db = {}
        self._autodumpdb()
        return True


__all__ = ["JsonDB"]
