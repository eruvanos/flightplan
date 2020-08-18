from typing import List

from pydantic import BaseModel, Field

from flightplan.render.task import Task, Step


class Job(BaseModel):
    name: str
    public: bool = False
    plan: List[Step] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # exclude list if unset, but allows adding new
        self.plan = list(self.plan)

    def add_task(self, task: Task):
        self.plan.append(task)