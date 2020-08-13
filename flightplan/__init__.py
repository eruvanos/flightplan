__version__ = '0.1.0'

from typing import List, Dict, Union

from pydantic import BaseModel, Field


class Stack:
    def __init__(self, *args):
        self.elements: List = list(args)

    def push(self, e):
        self.elements.append(e)

    def pop(self):
        return self.elements.pop()

    def peek(self):
        return self.elements[-1] if self.elements else None


stack = Stack()


class Command(BaseModel):
    path: str
    args: List[str]


class Source(BaseModel):
    repository: str
    tag: str


class ImageResource(BaseModel):
    type: str
    source: Source


class TaskConfig(BaseModel):
    platform: str
    image_resource: ImageResource
    run: Command

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        peek = stack.peek()
        if isinstance(peek, Task):
            peek.config = self

    def __enter__(self):
        stack.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if stack.pop() != self:
            raise Exception('Invalid state')


class Step(BaseModel):
    pass


class Get(Step):
    get: str = Field(alias='name')
    resource: str
    trigger: bool


class Put(Step):
    put: str = Field(alias='name')
    resource: str
    params: Dict[str, Union[int, str]]


class Task(Step):
    task: str = Field(alias='name')
    config: TaskConfig = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        peek = stack.peek()
        if isinstance(peek, Job):
            peek.add_task(self)

    def __enter__(self):
        stack.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if stack.pop() != self:
            raise Exception('Invalid state')


class Job(BaseModel):
    name: str
    public: bool = False
    plan: List[Step] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # exclude list if unset, but allows adding new
        self.plan = list(self.plan)

        peek = stack.peek()
        if isinstance(peek, Pipeline):
            peek.add_job(self)

    def add_task(self, task: Task):
        self.plan.append(task)

    def __enter__(self):
        stack.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if stack.pop() != self:
            raise Exception('Invalid state')


class Resource(BaseModel):
    name: str
    type: str
    source: Dict[str, Union[int, str]]


class ResourceType(BaseModel):
    name: str
    type: str
    source: Source


class Pipeline(BaseModel):
    name: str = Field(title='Title of the pipeline, not included in yaml')
    resource_types: List[ResourceType] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    jobs: List[Job] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # exclude list if unset, but allows adding new
        self.jobs = list(self.jobs)

    def add_job(self, job: Job):
        self.jobs.append(job)

    def __enter__(self):
        stack.push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if stack.pop() != self:
            raise Exception('Invalid state')

    def synth(self):
        return self.dict(
            exclude={'name'},
            exclude_unset=True
        )


__all__ = [
    'Job',
    'Get',
    'Put',
    'Task',
    'TaskConfig',
    'Source',
    'ImageResource',
    'Command',
    'Resource',
    'ResourceType',
    'Pipeline',
]
