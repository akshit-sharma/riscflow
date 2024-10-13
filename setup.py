from setuptools import setup, find_packages
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

setup(
    name='riscvflow',
    version=current_version,
    description='A library for control flow graph analysis of RISC-V assembly',
    author='Akshit Sharma',
    author_email='akshitsharma@mines.edu',
    packaes=find_packages(),
    install_requires=[
    ],
)
