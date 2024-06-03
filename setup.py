#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W6005,W6100
from __future__ import absolute_import, print_function

import os
import re
import sys

from setuptools import setup


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = get_version("drf_rw_serializers", "__init__.py")

if sys.argv[-1] == "tag":
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (VERSION, VERSION))
    os.system("git push --tags")
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
CHANGELOG = open(os.path.join(os.path.dirname(__file__), "CHANGELOG.rst")).read()

setup(
    name="drf-rw-serializers",
    version=VERSION,
    description=(
        "Generic views, viewsets and mixins that extend the Django REST "
        "Framework ones adding separated serializers for read and write operations"
    ),
    long_description=README + "\n\n" + CHANGELOG,
    long_description_content_type="text/x-rst",
    author="vintasoftware",
    author_email="contact@vinta.com.br",
    url="https://github.com/vintasoftware/drf-rw-serializers",
    packages=[
        "drf_rw_serializers",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=4.2,<6",
        "djangorestframework>=3.14,<4",
    ],
    license="MIT",
    zip_safe=False,
    keywords="Django REST Framework, Serializers, REST, API, Django",
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
