#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from common.constant import ALL_ENV_VARIABLE_FILES

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm56studios_be.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from common.utility import set_environment_variables
    for each_env_file in ALL_ENV_VARIABLE_FILES:
        set_environment_variables(env_file_path=each_env_file)
    main()
