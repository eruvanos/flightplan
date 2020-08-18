from typing import List, Dict, Union, Optional

from pydantic import BaseModel, Field

from flightplan.render.common import Source


class Command(BaseModel):
    path: str
    args: List[str] = Field(default_factory=list)


class ImageResource(BaseModel):
    type: str
    source: Source


class Mapping(BaseModel):
    name: str


class TaskConfig(BaseModel):
    platform: str
    image_resource: ImageResource
    run: Command
    inputs: List[Mapping] = Field(default_factory=list)
    outputs: List[Mapping] = Field(default_factory=list)


class Get(BaseModel):
    get: str
    passed: List[str] = Field(default_factory=list)
    resource: Optional[str] = None
    trigger: bool = False


class Put(BaseModel):
    put: str
    resource: Optional[str] = None
    params: Dict[str, Union[int, str]] = Field(default_factory=dict)


class Task(BaseModel):
    task: str
    config: TaskConfig


Step = Union[Get, Put, Task]
