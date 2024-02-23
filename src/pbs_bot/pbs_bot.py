# job_monitor.py

import os
import json
from pathlib import Path
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Job:
    def __init__(
            self,
            job_id,
            job_name,
            user_id,
            run_time,
            status,
            queue,

    ):
        self.job_id = job_id.split('.')[0]
        self.job_name = job_name
        self.user_id = user_id
        self.status = status
        self.queue = queue
        self.run_time = run_time



def get_qstat_job_info(
        job_id
):
    cmd = f'qstat {job_id}'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8')
    return output


def register_job(
        job_id
):
    qstat_job_info_output = get_qstat_job_info(job_id)
    job = Job(*qstat_job_info_output.splitlines()[2].split())
    pbs_bot_dir = Path(os.environ['HOME']) / '.pbs_bot'
    pbs_bot_dir.mkdir(parents=True, exist_ok=True)
    with open(pbs_bot_dir / 'jobs.json', 'r+') as f:
        registered_jobs = json.load(f)
        registered_jobs[job_id] = job.__dict__
        for k, v in registered_jobs.items():
            print(k, v)
    with open(pbs_bot_dir / 'jobs.json', 'w') as f:
        json.dump(registered_jobs, f)

