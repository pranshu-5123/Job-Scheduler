from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict


class Frequency(Enum):
    MINUTELY = "minutely"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class JobStatus(Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Job:
    def __init__(self, id: str, script_path: str, frequency: Frequency,
                 time_str: Optional[str] = None, day: Optional[str] = None):
        self.id = id
        self.script_path = script_path
        self.frequency = frequency
        self.time_str = time_str
        self.day = day
        self.status = JobStatus.SCHEDULED
        self.last_run = None
        self.history: List[Dict] = []
