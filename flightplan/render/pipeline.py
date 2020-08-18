from typing import Dict, Union, List, ClassVar

from pydantic import BaseModel, Field

from flightplan.render import Job
from flightplan.render.common import Source


class Resource(BaseModel):
    name: str
    type: str
    source: Dict[str, Union[int, str, list]]


class ResourceType(BaseModel):
    name: str
    type: str
    source: Source


class Pipeline(BaseModel):
    resource_types: List[ResourceType] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    jobs: List[Job] = Field(default_factory=list)

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
            exclude={'name'},
            exclude_unset=True
        )
