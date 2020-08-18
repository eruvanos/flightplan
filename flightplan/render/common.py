from typing import Union

from pydantic import BaseModel


class Source(BaseModel):
    repository: str
    tag: Union[int, str] = None
