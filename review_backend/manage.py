#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os # Import the os module for interacting with the operating system
import sys # Import the sys module for accessing command-line arguments
# Import the function to execute management commands
from django.core.management import execute_from_command_line  # pylint: disable=E0401


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "review_backend.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)

def main():
    """Run administrative tasks."""
    # Set the default Django settings module for the project
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "review_backend.settings")
    # Execute the command line utility with the provided arguments
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main() # Call the main function if the script is executed directly
