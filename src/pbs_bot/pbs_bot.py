# job_monitor.py

import os
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Job:
    def __init__(
            self,
            job_id,
            job_name,
            user_id,
            status,
            queue,
            run_time,

    ):
        self.job_id = job_id.split('.')[0]
        self.job_name = job_name
        self.user_id = user_id
        self.status = status
        self.queue = queue
        self.run_time = run_time


def parse_command_output(
        command_output
):
    lines = command_output.splitlines()
    lines = lines[2:]  # Skip headers
    jobs = []
    for line in lines:
        elements = line.split()
        job = Job(*elements)
        jobs.append(job)
    return jobs


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
    print(job.job_id, job.job_name, job.user_id, job.status, job.queue, job.run_time)