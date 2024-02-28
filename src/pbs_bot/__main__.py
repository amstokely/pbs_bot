# src/your_package_name/__main__.py
import sys

from .cli import config, register, _start, start, monitor_jobs

if __name__ == "__main__":
    if len(sys.argv):
        if sys.argv[1] == 'config':
            config()
        elif sys.argv[1] == 'register':
            register()
        elif sys.argv[1] == 'start':
            start()
        elif sys.argv[1] == '_start':
            _start()
