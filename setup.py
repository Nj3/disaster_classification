from distutils.core import setup
import os

from setuptools import PEP420PackageFinder

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

setup(
    name="disaster",
    version=1.0,
    description="Kaggle Getting started - NLP",
    author="Natarajan Subramanian",
    package_dir={"": "src"},
    packages=PEP420PackageFinder.find(where=str(SRC)),
)
