import pydantic
from pydantic.utils import ValueItems


class ReprMixin(pydantic.utils.Representation):
    """
    Add more options to Model representation
    """

    # def __repr__(self):
    #     return f'{self.__repr_name__()}({self.__repr_str__(", ")})'
    #
    # def __repr_str__(self, join_str: str) -> str:
    #     return join_str.join(repr(v) if a is None else f'{a}={v!r}' for a, v in self.__repr_args__())

    # TODO improve way of configuration
    def __repr_args__(
        self,
        to_dict: bool = False,
        by_alias: bool = False,
        include=None,
        exclude=None,
        exclude_unset: bool = False,
        exclude_defaults: bool = True,
        exclude_none: bool = True,
    ):
        from pydantic.main import _missing

        allowed_keys = self._calculate_keys(
            include=include, exclude=exclude, exclude_unset=exclude_unset
        )
        if allowed_keys is None and not (
            to_dict or by_alias or exclude_unset or exclude_defaults or exclude_none
        ):
            # huge boost for plain _iter()
            yield from self.__dict__.items()
            return

        value_exclude = ValueItems(self, exclude) if exclude else None
        value_include = ValueItems(self, include) if include else None

        for field_key, v in self.__dict__.items():
            if (
                (allowed_keys is not None and field_key not in allowed_keys)
                or (exclude_none and v is None)
                or (
                    exclude_defaults
                    and self.__field_defaults__.get(field_key, _missing) == v
                )
            ):
                continue
            if by_alias and field_key in self.__fields__:
                dict_key = self.__fields__[field_key].alias
            else:
                dict_key = field_key
            if to_dict or value_include or value_exclude:
                v = self._get_value(
                    v,
                    to_dict=to_dict,
                    by_alias=by_alias,
                    include=value_include and value_include.for_element(field_key),
                    exclude=value_exclude and value_exclude.for_element(field_key),
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            yield dict_key, v


class BaseModel(ReprMixin, pydantic.BaseModel):
    """
    Drop in replacement for pydantic.BaseModel with better representation
    """

    pass
