from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="progress-bar",
    description="A package for simple progress bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Fan Rende",
    package_dir={"": "src"},
    version="0.1.0",
    packages=find_packages(where="src"),
)