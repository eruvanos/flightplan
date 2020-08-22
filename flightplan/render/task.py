from enum import Enum
from typing import List, Dict, Union, Optional, ForwardRef

from pydantic import Field

from flightplan.render.utils import BaseModel


class Command(BaseModel):
    path: str
    args: Optional[List[str]] = None
    dir: Optional[str] = None
    user: Optional[str] = None


class ImageResource(BaseModel):
    type: str
    source: Dict
    params: Optional[Dict]
    version: Optional[Dict[str, str]]


class Input(BaseModel):
    name: str
    path: Optional[str] = None
    optional: Optional[bool] = None


class Output(BaseModel):
    name: str
    path: Optional[str] = None


class Cache(BaseModel):
    path: str


class ContainerLimits(BaseModel):
    cpu: Optional[int] = None
    memory: Optional[int] = None


class TaskConfig(BaseModel):
    platform: str
    image_resource: ImageResource
    inputs: Optional[List[Input]] = None
    outputs: Optional[List[Output]] = None
    caches: Optional[List[Cache]] = None
    params: Optional[Dict] = None
    run: Command
    rootfs_uri: Optional[str] = None
    container_limits: Optional[ContainerLimits] = None


# Create ForwardRefs for all step types
Get = ForwardRef("Get")
Put = ForwardRef("Put")
Task = ForwardRef("Task")
SetPipeline = ForwardRef("SetPipeline")
Do = ForwardRef("Do")
Try = ForwardRef("Try")
InParallel = ForwardRef("InParallel")
LoadVar = ForwardRef("LoadVar")
Step = Union[Get, Put, Task, SetPipeline, Do, Try, InParallel, LoadVar]


class _Step(BaseModel):
    """
    Base class for all steps, contains common attributes.
    """

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class GetVersion(str, Enum):
    latest = "latest"
    every = "every"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class Get(BaseModel):
    class Config:
        use_enum_values = True

    get: str
    resource: Optional[str] = None
    passed: List[str] = None
    params: Dict = None
    trigger: bool = False
    version: Optional[Union[GetVersion, Dict[str, str]]] = GetVersion.latest

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class PutInput(str, Enum):
    all = "all"
    detect = "detect"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class Put(BaseModel):
    class Config:
        use_enum_values = True

    put: str
    resource: Optional[str] = None
    inputs: Optional[Union[PutInput, List[str]]] = None
    params: Dict = None
    get_params: Dict = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class Task(_Step):
    task: str
    config: Optional[TaskConfig] = None
    file: Optional[str] = None
    image: Optional[str] = None
    privileged: bool = False

    vars: Dict = None
    params: Dict = None
    input_mapping: Dict[str, str] = None
    output_mapping: Dict[str, str] = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class SetPipeline(BaseModel):
    set_pipeline: str
    file: str
    vars: Optional[Dict] = None
    var_files: Optional[List[str]] = None
    team: Optional[str] = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class Format(str, Enum):
    json = "json"
    yaml = "yaml"
    yml = "yml"
    trim = "trim"
    raw = "raw"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class LoadVar(BaseModel):
    class Config:
        use_enum_values = True

    load_var: str
    file: str
    format: Optional[Format] = None
    reveal: Optional[bool] = None


class Do(BaseModel):
    do: List[Step]
    file: Optional[str] = None
    vars: Dict = None
    params: Dict = None
    team: Optional[str] = None

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None


class Try(BaseModel):
    class Config:
        allow_population_by_field_name = True

    try_: Step = Field(alias="try")

    # Common fields,
    timeout: Optional[str] = None
    attempts: Optional[int] = None
    tags: Optional[List[str]] = None
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
    tags: Optional[List[str]] = None
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
LoadVar.update_forward_refs()

# Redefine step with set up models (update_forward_refs)
Step = Union[Get, Put, Task, SetPipeline, Do, Try, InParallel, LoadVar]
