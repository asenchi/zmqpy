import os
import sys

from setuptools import setup, find_packages, Command

VERSION = __import__("zmq").__version__

install_requires = []
try:
    import importlib
except ImportError:
    install_requires.append("importlib")

is_cpy = sys.version_info
is_pypy = hasattr(sys, "pypy_version_info")

setup(
    name="python-zmq",
    version=VERSION,
    description="Pure Python 0mq bindings.",
    license="MIT",
    url="https://github.com/asenchi/python-zmq",
    author="Curt Micol",
    author_email="asenchi@asenchi.com",
    zip_safe=False,
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Topic :: Software Development :: Libraries :: Application Frameworks",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
    ],
    test_suite='zmq.tests',
)
