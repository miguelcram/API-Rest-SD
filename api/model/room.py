from typing import Any, Dict

from api.exeptions import ValidationError


class Room(object):
    field_types = {'booked': bool, 'capacity': int, 'equipment': list}

    def __init__(self, **kwargs: Dict[str, Any]):
        self.booked = kwargs.get('booked', None)
        self.capacity = kwargs.get('capacity', None)
        self.equipment = kwargs.get('equipment', None)
        Room._validate(self.__dict__.items())
        self.id = kwargs.get('id', None)

    @staticmethod
    def _validate(fields):
        errors = {}
        for attr, value in fields:
            if attr in Room.field_types.keys():
                if value is None:
                    errors[attr] = "{} is required".format(attr)
                elif not isinstance(value, Room.field_types[attr]):
                    if (isinstance(value, list) and len(value) > 0
                            and not isinstance(value[0], str)):
                        errors[attr] = "{} elements type must be str".format(
                            attr)
                    else:
                        errors[attr] = "{} type must be {}".format(
                            attr, Room.field_types[attr].__name__)

        if len(errors) > 0:
            raise ValidationError(errors=errors)

    @staticmethod
    def validate_update(**kwargs: Dict[str, Any]):
        Room._validate(kwargs.items())
