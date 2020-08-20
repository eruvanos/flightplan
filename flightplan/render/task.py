from enum import Enum
from typing import List, Dict, Union, Optional, ForwardRef

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
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)


# Create ForwardRefs for all step types
Get = ForwardRef('Get')
Put = ForwardRef('Put')
Task = ForwardRef('Task')
SetPipeline = ForwardRef('SetPipeline')
Do = ForwardRef('Do')
Try = ForwardRef('Try')
InParallel = ForwardRef('InParallel')
Step = Union[Get, Put, Task, SetPipeline, Do, Try, InParallel]


class _Step(BaseModel):
    """
    Base class for all steps, contains common attributes.
    """

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class GetVersion(str, Enum):
    latest = 'latest'
    every = 'every'

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


class Get(BaseModel):
    class Config:
        use_enum_values = True

    get: str
    resource: Optional[str] = None
    passed: List[str] = Field(default_factory=list)
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    trigger: bool = False
    version: Optional[GetVersion] = GetVersion.latest.value

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class PutInput(str, Enum):
    all = 'all'
    detect = 'detect'

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


class Put(BaseModel):
    class Config:
        use_enum_values = True

    put: str
    resource: Optional[str] = None
    inputs: Optional[PutInput] = PutInput.all
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    get_params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class Task(_Step):
    task: str
    config: Optional[TaskConfig] = None
    file: Optional[str] = None
    # TODO image https://concourse-ci.org/jobs.html#schema.step.task-step.image
    privileged: bool = False

    vars: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    input_mapping: Dict[str, str] = Field(default_factory=dict)
    output_mapping: Dict[str, str] = Field(default_factory=dict)

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None



class SetPipeline(BaseModel):
    set_pipeline: str
    file: Optional[str] = None
    vars: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    team: Optional[str] = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


# TODO Load_vars: https://concourse-ci.org/jobs.html#schema.step.load-var-step.load_var


class Do(BaseModel):
    do: List[Step]
    file: Optional[str] = None
    vars: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    team: Optional[str] = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class Try(BaseModel):
    class Config:
        allow_population_by_field_name = True

    try_: Step = Field(alias='try')

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class InParallelConfig(BaseModel):
    steps: List[Step]
    limit: Optional[int] = None
    fail_fast: bool = False


class InParallel(BaseModel):
    in_parallel: InParallelConfig

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


# https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Get.update_forward_refs()
Put.update_forward_refs()
Task.update_forward_refs()
SetPipeline.update_forward_refs()
Do.update_forward_refs()
Try.update_forward_refs()
InParallelConfig.update_forward_refs()
InParallel.update_forward_refs()

# Redefine step with set up models (update_forward_refs)
Step = Union[Get, Put, Task, SetPipeline, Do, Try, InParallel]
