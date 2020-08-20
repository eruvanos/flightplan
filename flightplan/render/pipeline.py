from typing import Dict, Union, List, ClassVar, Optional

from pydantic import BaseModel, Field

from flightplan.render import Job
from flightplan.render.common import Source

# TODO fix handling of default list and dict

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
    privileged: Optional[bool]
    params: Dict[str, Union[bool, int, str, list, dict]] = Field(default_factory=dict)
    check_every: Optional[str]
    tags: Optional[List[str]]
    unique_version_history: Optional[bool]


class Pipeline(BaseModel):
    jobs: List[Job] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    resource_types: List[ResourceType] = Field(default_factory=list)
    # var_source: # TODO https://concourse-ci.org/pipelines.html#schema.pipeline.var_sources
    groups: Optional[Dict[str, List[str]]] = Field(default_factory=list)

    pipelines: ClassVar[List['Pipeline']] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # exclude list if unset, but allows adding new
        # self.jobs = list(self.jobs)
        Pipeline.pipelines.append(self)

    def add_job(self, job: Job):
        self.jobs.append(job)

    def add_resource_type(self, resource_type: ResourceType):
        self.resource_types.append(resource_type)

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def synth(self):
        return self.dict(
            by_alias=True,
            exclude={'name'},
            exclude_unset=True
        )
