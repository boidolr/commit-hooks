import sys
from setuptools import setup

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []
requirements = open("requirements.txt").readlines()
requirements_test = open("requirements-dev.txt").readlines()

setup(
    install_requires=requirements,
    setup_requires=pytest_runner,
    tests_require=requirements_test,
)
