# cli.py
import os
import subprocess
import sys
from pathlib import Path

from pbs_bot.secrets import encrypt_slack_token
from pbs_bot import register_job, monitor_jobs
from .pbs_bot_io import pbs_bot_dir
import json


def config():
    slack_token = sys.argv[2]
    slack_user_id = sys.argv[3]
    key = sys.argv[4]
    config_file = pbs_bot_dir / "config.json"
    with open(config_file, 'w') as f:
        json.dump(
            {'slack_token': encrypt_slack_token(slack_token, key=key),
             'slack_user_id': encrypt_slack_token(
                 slack_user_id, key=key),
             }, f)


def register():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m pbs_bot <job_id>")
        sys.exit(1)

    job_id = sys.argv[2]
    register_job(job_id)


def listen():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m listen <key>")
        sys.exit(1)
    key = sys.argv[2]
    monitor_jobs(key)


def start():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m start <key>")
        sys.exit(1)
    key = sys.argv[2]
    subprocess.run(['tmux', 'new-session', '-d', '-s', 'pbs_bot'])
    subprocess.run(['tmux', 'send-keys', '-t', 'pbs_bot', f'python -m pbs_bot _start {key}', 'Enter'])


def _start():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m _start <key>")
        sys.exit(1)
    key = sys.argv[2]
    subprocess.run(['tmux', 'send-keys', '-t', 'pbs_bot', f'python -m pbs_bot listen {key}', 'Enter'])
