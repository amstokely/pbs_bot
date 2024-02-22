# job_monitor.py

import os
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class PBSJobMonitor:
    def __init__(
            self,
            userid,
            jobname,
            slack_channel_id,
            slack_token
            ):
        self.userid = userid
        self.jobname = jobname
        self.slack_channel_id = slack_channel_id
        self.slack_token = slack_token

    class Job:
        def __init__(
                self,
                job_id,
                username,
                queue,
                jobname,
                sessid,
                nds,
                tsk,
                memory,
                time,
                s,
                elap_time
        ):
            self.job_id = job_id
            self.username = username
            self.queue = queue
            self.jobname = jobname
            self.sessid = sessid
            self.nds = nds
            self.tsk = tsk
            self.memory = memory
            self.time = time
            self.s = s
            self.elap_time = elap_time

    def parse_command_output(
            self,
            command_output
            ):
        lines = command_output.splitlines()
        lines = lines[3:]  # Skip headers
        jobs = []
        for line in lines:
            elements = line.split()
            job = self.Job(*elements)
            jobs.append(job)
        return jobs

    def get_qstat_job_status(
            self
            ):
        cmd = f'qstat -u {self.userid}'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        output = result.stdout.decode('utf-8')
        return output

    def monitor_jobs_and_notify(
            self
            ):
        job_started = False
        while not job_started:
            job_status = self.get_qstat_job_status()
            client = WebClient(token=self.slack_token)
            jobs = self.parse_command_output(job_status)
            for job in jobs:
                if job.jobname.startswith(self.jobname):
                    job_str = f"{job.job_id}    {job.jobname}    {job.s}    {job.elap_time}\n"
                    print(job_str)
                    if job.elap_time != '--':
                        try:
                            response = client.chat_postMessage(
                                channel=self.slack_channel_id,
                                text=job_str)
                            assert response["message"][
                                       "text"] == job_str
                        except SlackApiError as e:
                            print(f"Error sending message: {e}")
                        job_started = True
                        break
