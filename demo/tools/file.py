import json


def read_from_file(filename):
    """Read content from a file and return it."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."

def write_to_file(filename, content):
    """Write given content to a file."""
    with open(filename, 'w') as file:
        file.write(content)