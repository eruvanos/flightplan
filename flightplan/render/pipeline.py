from enum import Enum
from typing import Dict, List, ClassVar, Optional, Union

from flightplan.render.job import Job
from flightplan.render.utils import BaseModel, enum_values
from flightplan.render.var import Var


class Resource(BaseModel):
    name: str
    type: str
    source: Dict
    old_name: Optional[str] = None
    icon: Optional[str] = None
    version: Optional[Union[Var, Dict[str, str]]] = None
    check_every: Optional[str] = None
    tags: Optional[List[str]] = None
    public: Optional[Union[Var, bool]] = None
    webhook_token: Optional[str] = None


class ResourceType(BaseModel):
    name: str
    type: str
    source: Dict
    privileged: Optional[Union[Var, bool]] = None
    params: Optional[Dict] = None
    check_every: Optional[str] = None
    tags: Optional[List[str]] = None
    unique_version_history: Optional[Union[Var, bool]] = None


class GroupConfig(BaseModel):
    name: str
    jobs: Optional[List[str]] = None


class VarSourceType(str, Enum):
    vault = "vault"
    dummy = "dummy"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class VarSource(BaseModel):
    name: str
    type: VarSourceType
    config: Dict


class Pipeline(BaseModel):
    jobs: Optional[List[Job]] = None
    resources: Optional[List[Resource]] = None
    resource_types: Optional[List[ResourceType]] = None
    var_source: Optional[VarSource] = None
    groups: Optional[List[GroupConfig]] = None

    pipelines: ClassVar[List["Pipeline"]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Pipeline.pipelines.append(self)

    def add_job(self, job: Job):
        if self.jobs is None:
            self.jobs = []
        self.jobs.append(job)

    def add_resource_type(self, resource_type: ResourceType):
        if self.resource_types is None:
            self.resource_types = []
        self.resource_types.append(resource_type)

    def add_resource(self, resource: Resource):
        if self.resources is None:
            self.resources = []
        self.resources.append(resource)

    def synth(self):
        return enum_values(
            self.model_dump(
                by_alias=True,
                exclude={"name"},
                exclude_unset=True,
                # exclude_none=True,
                # exclude_defaults=True,
            )
        )
