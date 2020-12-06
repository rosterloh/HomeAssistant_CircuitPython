"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="homeassistant-circuitpython",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Home Assistant library for CircuitPython",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project's main homepage.
    url="https://github.com/rosterloh/HomeAssistant_CircuitPython",
    # Author details
    author="Richard Osterloh",
    author_email="richard.osterloh@gmail.com",
    install_requires=[
        "adafruit-blinka",
        "adafruit-circuitpython-minimqtt"
    ],
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # What does your project relate to?
    keywords="adafruit blinka circuitpython micropython homeassistant",
    packages=find_packages(include=["homeassistant", "homeassistant.*"]),
)