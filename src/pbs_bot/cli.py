# cli.py
import os
import sys
from pathlib import Path

#from pbs_bot import PBSJobMonitor
from pbs_bot.secrets import encrypt_slack_token
from pbs_bot.secrets import decrypt_slack_token
from pbs_bot import register_job
import json


def config():
    config_dir = Path(os.environ['HOME']) / '.config' / 'pbs_bot'
    config_dir.mkdir(parents=True, exist_ok=True)
    slack_token = sys.argv[2]
    slack_user_id = sys.argv[3]
    key = sys.argv[4]
    with open(config_dir / 'pbs_bot_config.json', 'w') as f:
        json.dump(
            {'slack_token': encrypt_slack_token(slack_token, key=key),
             'slack_user_id': encrypt_slack_token(
                 slack_user_id, key=key),
             }, f)


def register():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m pbs_bot <job_id> <key>")
        sys.exit(1)

    job_id, key = sys.argv[1:]
    config_dir = Path(os.environ['HOME']) / '.config' / 'pbs_bot'
    with open(config_dir / 'pbs_bot_config.json', 'r') as f:
        config = json.load(f)
        slack_token = decrypt_slack_token(config['slack_token'], key=key)
        slack_user_id = decrypt_slack_token(config['slack_user_id'], key=key)
    register_job(job_id)
