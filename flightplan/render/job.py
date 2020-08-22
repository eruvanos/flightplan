from typing import List

from flightplan.render.task import Task, Step
from flightplan.render.utils import BaseModel


class Job(BaseModel):
    name: str
    public: bool = False
    serial: bool = False
    plan: List[Step] = None

    class Config:
        use_enum_values = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self, task: Task):
        self.plan = list(self.plan)  # FIXME the unset problem
        self.plan.append(task)
