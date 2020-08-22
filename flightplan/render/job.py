from typing import List, Optional

from flightplan.render.task import Task, Step
from flightplan.render.utils import BaseModel


class BuildLogRetentionPolicy(BaseModel):
    days: Optional[int] = None
    builds: Optional[int] = None
    minimum_succeeded_builds: Optional[int] = None


class Job(BaseModel):
    name: str
    plan: List[Step] = None

    old_name: Optional[str]
    serial: Optional[bool] = None
    build_log_retention: Optional[BuildLogRetentionPolicy] = None
    build_logs_to_retain: Optional[int] = None
    serial_groups: Optional[List[str]] = None
    max_in_flight: Optional[int] = None
    public: Optional[bool] = None
    disable_manual_trigger: Optional[bool] = None
    interruptible: Optional[bool] = None
    on_success: Optional[Step] = None
    on_failure: Optional[Step] = None
    on_abort: Optional[Step] = None
    on_error: Optional[Step] = None
    ensure: Optional[Step] = None

    class Config:
        use_enum_values = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self, task: Task):
        if self.plan is None:
            self.plan = []
        self.plan.append(task)
