import re

from pydantic_core import core_schema

_variable_matcher = r"^\(\(.*\)\)$"
_variable_regex = re.compile(_variable_matcher)


class Var(str):
    """
    Concourse variable, workaround for fields that normally require a non-string type
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        json_schema = handler(schema)
        json_schema.update(
            pattern=_variable_matcher, examples=["((my-secret))"],
        )
        return json_schema

    @classmethod
    def validate(cls, v):
        m = _variable_regex.fullmatch(v)
        if not m:
            raise ValueError("invalid secret format")
        return cls(v)

    def __repr__(self):
        return f"Var({super().__repr__()})"
