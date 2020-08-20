from typing import List

from pydantic import BaseModel, Field

from flightplan.render.task import Task, Step


class Job(BaseModel):
    name: str
    public: bool = False
    serial: bool = False
    plan: List[Step] = Field(default_factory=list)

    class Config:
        use_enum_values = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self, task: Task):
        self.plan = list(self.plan)  # FIXME the unset problem
        self.plan.append(task)
