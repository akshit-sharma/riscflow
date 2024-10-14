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
    packages=find_packages(),
    install_requires=[
        'graphviz',
    ],
    entry_points={
        'console_scripts': [
            'risvflow-print-functions=riscvflow.main.print_functions:main',
            'riscvflow-generate-cfg=riscvflow.main.generate_cfg:main',
            'riscvflow-register-usage=riscvflow.main.register_usage:main',
            'riscvflow-graphviz-functions=riscvflow.main.graphviz_functions:main',
        ],
    },
)
