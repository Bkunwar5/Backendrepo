
from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.28.0",
        "moto>=5.0.0",
        "pytest>=8.0.0"
    ],
)