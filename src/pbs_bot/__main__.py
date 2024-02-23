# src/your_package_name/__main__.py
import sys

from .cli import register_job
from .cli import config

if __name__ == "__main__":
    if len(sys.argv) and sys.argv[1] == 'config':
        config()
    else:
        register_job()
