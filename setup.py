from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="mortalprogressbar",
    description="A package for simple progress bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zxcj04/Progress-bar",
    author="FanRende Huang",
    package_dir={"": "src"},
    version="1.0.1",
    packages=find_packages(where="src"),
)