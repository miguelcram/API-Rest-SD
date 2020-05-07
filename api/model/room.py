from typing import Any, Dict
from api.exeptions import ValidationError


class Room(object):
    field_types = {'booked': bool, 'capacity': int, 'equipment': list}

    def __init__(self, **kwargs: Dict[str, Any]):
        print(kwargs)
        self.booked = kwargs.get('booked', None)
        self.capacity = kwargs.get('capacity', None)
        self.equipment = kwargs.get('equipment', None)
        self._validate()
        self.id = None

    def _validate(self):
        errors = {}
        for attr, value in self.__dict__.items():
            if value is None:
                errors[attr] = "{} is required".format(attr)

            elif not isinstance(value, self.field_types[attr]):

                if (isinstance(value, list) and len(value) > 0
                        and not isinstance(value[0], str)):
                    errors[attr] = "{} elements type must be str".format(attr)

                errors[attr] = "{} type must be {}".format(
                    attr, self.field_types[attr].__name__)

        if len(errors) > 0:
            raise ValidationError(errors=errors)
