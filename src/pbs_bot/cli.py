# cli.py
import os
import sys
from pathlib import Path

from pbs_bot import PBSJobMonitor
from pbs_bot.secrets import encrypt_slack_token
from pbs_bot.secrets import decrypt_slack_token
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


def register_job():
    if len(sys.argv) != 4:
        print(
            "Usage: main.py <userid> <jobname> <key>")
        sys.exit(1)

    userid, jobname, key = sys.argv[1:]
    config_dir = Path(os.environ['HOME']) / '.config' / 'pbs_bot'
    with open(config_dir / 'pbs_bot_config.json', 'r') as f:
        config = json.load(f)
        slack_token = decrypt_slack_token(config['slack_token'], key=key)
        slack_user_id = decrypt_slack_token(config['slack_user_id'], key=key)
    monitor = PBSJobMonitor(userid, jobname, slack_user_id,
                            slack_token)
    print(slack_token, slack_user_id, userid, jobname)
    # monitor.monitor_jobs_and_notify()
