# job_monitor.py

import os
import json
from pathlib import Path
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .pbs_bot_io import pbs_bot_dir


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
    jobs_file = pbs_bot_dir / "jobs.json"
    jobs = {}
    if jobs_file.exists() and jobs_file.stat().st_size != 0:
        with open(jobs_file, 'r+') as f:
            jobs.update(json.load(f))
    jobs[job_id] = job.__dict__
    with open(jobs_file, 'w') as f:
        json.dump(jobs, f)


def post_job_to_slack(job_dict, key):

    
    client = WebClient(token=slack_token)

    channel_id = "YOUR_CHANNEL_ID"  # ID of the channel you want to send message to
    message = "Hello, world!"  # Your message

    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
        # In case of error, print it out
        print(f"Error sending message: {e}")


def monitor_jobs(key):
    jobs_file = pbs_bot_dir / "jobs.json"
    jobs = {}
    if jobs_file.exists() and jobs_file.stat().st_size != 0:
        with open(jobs_file, 'r+') as f:
            jobs.update(json.load(f))
    for job_id, job in jobs.items():
        post_job_to_slack(job_id, key)
