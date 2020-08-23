import re

_variable_matcher = r"^\(\(.*\)\)$"
_variable_regex = re.compile(_variable_matcher)


class Var(str):
    """
    Concourse variable, workaround for fields that normally require a non-string type
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=_variable_matcher, examples=["((my-secret))"],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        m = _variable_regex.fullmatch(v)
        if not m:
            raise ValueError("invalid secret format")
        return cls(v)

    def __repr__(self):
        return f"Var({super().__repr__()})"
