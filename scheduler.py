import json
import os
import subprocess
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

import schedule

from models import Job, Frequency, JobStatus
from utilities import validate_script_path, setup_logger


class AdvancedJobScheduler:
    def __init__(self, jobs_file="jobs.json"):
        self.jobs: Dict[str, Job] = {}
        self.scheduler = schedule.Scheduler()
        self.running = False
        self.logger = setup_logger('JobScheduler')
        self.jobs_file = jobs_file
        self.load_jobs()

    def save_jobs(self):
        data = {
            job_id: {
                "script_path": job.script_path,
                "frequency": job.frequency.value,
                "time_str": job.time_str,
                "day": job.day
            }
            for job_id, job in self.jobs.items()
        }
        with open(self.jobs_file, "w") as f:
            json.dump(data, f)

    def load_jobs(self):
        if os.path.exists(self.jobs_file):
            with open(self.jobs_file, "r") as f:
                data = json.load(f)
                for job_id, job_info in data.items():
                    self.schedule_job(
                        job_id,
                        job_info["script_path"],
                        Frequency[job_info["frequency"].upper()],
                        job_info.get("time_str"),
                        job_info.get("day")
                    )

    def execute_script(job: Job):
        job.status = JobStatus.RUNNING
        job.last_run = datetime.now()

        print(f"Executing scheduled job: {job.id} - {job.script_path}")  # CLI message

        try:
            # Adjust command based on file type
            if job.script_path.endswith('.py'):
                command = ['python', job.script_path]
            elif job.script_path.endswith('.sh'):
                command = ['bash', job.script_path]
            else:
                command = [job.script_path]

            result = subprocess.run(command, capture_output=True, text=True)

            execution_record = {
                "timestamp": job.last_run.isoformat(),
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout.strip(),
                "error": result.stderr.strip()
            }

            if result.returncode == 0:
                job.status = JobStatus.COMPLETED
                print(f"Job {job.id} executed successfully.")
            else:
                job.status = JobStatus.FAILED
                print(f"Job {job.id} failed. Error: {result.stderr}")

        except Exception as e:
            execution_record = {
                "timestamp": job.last_run.isoformat(),
                "status": "failed",
                "output": "",
                "error": str(e)
            }
            job.status = JobStatus.FAILED
            print(f"Job {job.id} encountered an error: {str(e)}")

        # Append execution record to history
        job.history.append(execution_record)
        job.status = JobStatus.SCHEDULED

    def save_job_history_to_file(self, job: Job):
        log_file = f"{job.id}_history.log"
        with open(log_file, "a") as f:
            for record in job.history[-1:]:  # Only save the latest record
                f.write(json.dumps(record, indent=4) + "\n")

    def remove_job(self, job_id: str):
        """
        Removes a scheduled job by its ID.
        """
        if job_id not in self.jobs:
            print(f"Job {job_id} does not exist.")
            return

        # Remove job from the scheduler
        job = self.jobs[job_id]
        try:
            self.scheduler.cancel_job(job)
            del self.jobs[job_id]
            self.save_jobs()
            print(f"Job {job_id} removed successfully.")
        except Exception as e:
            print(f"Error removing job {job_id}: {e}")


    def view_job_history(self):
        job_id = input("Enter the job ID to view history: ")
        if job_id not in self.jobs:
            print("Invalid job ID.")
            return

        job = self.jobs[job_id]
        print(f"History for Job ID: {job.id}")
        if not job.history:
            print("No execution history available.")
            return

        for record in job.history:
            print(f"Timestamp: {record['timestamp']}")
            print(f"Status: {record['status']}")
            if record['output']:
                print(f"Output: {record['output']}")
            if record['error']:
                print(f"Error: {record['error']}")
            print("-" * 40)

    def schedule_job(self, job_id: str, script_path: str, frequency: Frequency,
                     time_str: Optional[str] = None, day: Optional[str] = None):
        if not os.path.isfile(script_path):
            raise ValueError(f"Invalid script path: {script_path}. File does not exist.")
        if not os.access(script_path, os.X_OK):
            print(f"Warning: {script_path} is not marked as executable. Make sure it's a valid file.")
        if job_id in self.jobs:
            raise ValueError(f"Job {job_id} already exists")

        if not validate_script_path(script_path):
            self.logger.warning(f"Invalid script path: {script_path}")
            return

        job = Job(job_id, script_path, frequency, time_str, day)
        schedule_conf = self.scheduler.every()

        if frequency == Frequency.MINUTELY:
            schedule_conf.minute.do(self.execute_script, job)
        elif frequency == Frequency.HOURLY:
            schedule_conf.hour.do(self.execute_script, job)
        elif frequency == Frequency.DAILY:
            if time_str:
                schedule_conf.day.at(time_str).do(self.execute_script, job)
            else:
                schedule_conf.day.do(self.execute_script, job)

        self.jobs[job_id] = job
        self.save_jobs()

    def list_jobs(self) -> List[str]:
        return [
            f"{job.id}: {job.frequency.value}, {job.script_path}"
            for job in self.jobs.values()
        ]

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._run)
        thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            self.scheduler.run_pending()
            time.sleep(1)
