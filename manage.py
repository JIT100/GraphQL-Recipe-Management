#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Default to the consolidated settings package; it will switch
    # between development/production based on the DEBUG env.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)
