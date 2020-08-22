from enum import Enum
from typing import Dict, List, ClassVar, Optional, Any

from flightplan.render.job import Job
from flightplan.render.task import Get, Put, LoadVar
from flightplan.render.utils import BaseModel


class Resource(BaseModel):
    name: str
    type: str
    source: Dict
    old_name: Optional[str]
    icon: Optional[str]
    version: Optional[Dict[str, str]]
    check_every: Optional[str]
    tags: Optional[List[str]]
    public: Optional[bool]
    webhook_token: Optional[str]


class ResourceType(BaseModel):
    name: str
    type: str
    source: Dict
    privileged: Optional[bool] = None
    params: Optional[Dict] = None
    check_every: Optional[str] = None
    tags: Optional[List[str]] = None
    unique_version_history: Optional[bool] = None


class GroupConfig(BaseModel):
    name: str
    jobs: Optional[List[str]] = None


class VarSourceType(str, Enum):
    vault = "vault"
    dummy = "dummy"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class VarSource(BaseModel):
    class Config:
        use_enum_values = True

    name: str
    type: VarSourceType
    config: Dict


class Pipeline(BaseModel):
    jobs: List[Job] = None
    resources: List[Resource] = None
    resource_types: List[ResourceType] = None
    var_source: Optional[VarSource]
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
        return self.dict(
            by_alias=True,
            exclude={"name"},
            exclude_unset=True,
            # exclude_none=True,
            # exclude_defaults=True,
        )

    @classmethod
    def parse_obj(cls, obj: Any) -> "Pipeline":
        models_contain_enum = [Get, Put, LoadVar, VarSource]

        # Disable Enum representation as string
        for model in models_contain_enum:
            model.Config.use_enum_values = False

        result = super().parse_obj(obj)

        # Enable Enum representation as string
        for model in models_contain_enum:
            model.Config.use_enum_values = True

        return result
