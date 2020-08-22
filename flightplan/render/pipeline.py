from typing import Dict, Union, List, ClassVar, Optional

from flightplan.render import Job
from flightplan.render.common import Source

# TODO fix handling of default list and dict
from flightplan.render.utils import BaseModel


class Resource(BaseModel):
    name: str
    type: str
    source: Dict[str, Union[int, str, list]]
    old_name: Optional[str]
    icon: Optional[str]
    # version: # TODO https://concourse-ci.org/resources.html#schema.resource.version
    check_every: Optional[str]
    tags: Optional[List[str]]
    public: Optional[bool]
    webhook_token: Optional[str]


class ResourceType(BaseModel):
    name: str
    type: str
    source: Source
    privileged: Optional[bool] = None
    params: Dict[str, Union[bool, int, str, list, dict]] = None
    check_every: Optional[str] = None
    tags: Optional[List[str]] = None
    unique_version_history: Optional[bool] = None


class Pipeline(BaseModel):
    jobs: List[Job] = None
    resources: List[Resource] = None
    resource_types: List[ResourceType] = None
    # var_source: # TODO https://concourse-ci.org/pipelines.html#schema.pipeline.var_sources
    groups: Optional[Dict[str, List[str]]] = None

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
            # exclude_unset=True,
            # exclude_none=True,
            exclude_defaults=True,
        )
