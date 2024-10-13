from pathlib import Path
import re

current_version_regex = re.compile(r'current_version\s*=\s*\"(\d+\.\d+\.\d+)\"')

with open(Path(__file__).parent / '.bumpversion.toml', 'r') as f:
    bumpversion_toml = f.read()
    for line in bumpversion_toml.split('\n'):
        match = current_version_regex.match(line)
        if match:
            current_version = match.group(1)
            break

__version__ = current_version
