# cli.py

import sys
from pbs_bot import PBSJobMonitor

def main():
    if len(sys.argv) != 5:
        print("Usage: python -m pbs_bot <userid> <jobname> "
              "<slack_channel_id> <slack_token>")

        sys.exit(1)

    userid, jobname, slack_channel_id, slack_token = sys.argv[1:]
    monitor = PBSJobMonitor(userid, jobname, slack_channel_id, slack_token)
    monitor.monitor_jobs_and_notify()

if __name__ == "__main__":
    main()
