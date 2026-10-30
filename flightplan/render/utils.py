from enum import Enum

import pydantic


class BaseModel(pydantic.BaseModel):
    """
    Drop in replacement for pydantic.BaseModel with better representation
    """

    def __repr_args__(self):
        # Only show fields that were explicitly set and are not None
        for name in type(self).model_fields:
            if name not in self.model_fields_set:
                continue
            value = getattr(self, name)
            if value is not None:
                yield name, value


def enum_values(data):
    """
    Recursively replace Enum members with their values
    """
    if isinstance(data, Enum):
        return data.value
    if isinstance(data, dict):
        return {k: enum_values(v) for k, v in data.items()}
    if isinstance(data, list):
        return [enum_values(v) for v in data]
    return data
