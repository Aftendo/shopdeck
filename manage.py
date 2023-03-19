#!/usr/bin/env python
'''
API & Metadata server
Made by Let's Shop! 2023
'''
import os
import sys

print("Shopdeck Server - API & Web Portal\n\nBy Let's Shop Team 2023")
print("----------------------------------")
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopdeck.settings')
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
    main()
