import os

from pathlib import Path


def __pbs_bot_dir():
    pbs_bot_dir_ = Path(os.environ["HOME"]) / ".pbs_bot"
    pbs_bot_dir_.mkdir(exist_ok=True)
    return pbs_bot_dir_


pbs_bot_dir = __pbs_bot_dir()
