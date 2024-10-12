from setuptools import setup, find_packages
from pathlib import Path

version = {}
with open(Path(__file__).parent / 'riscvflow' / '__version__.py') as fp:
    exec(fp.read(), version)

setup(
    name='riscvflow',
    version=version['__version__'],
    description='A library for control flow graph analysis of RISC-V assembly',
    author='Akshit Sharma',
    author_email='akshitsharma@mines.edu',
    packaes=find_packages(),
    install_requires=[
    ],
)
