#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup

with io.open("fluent/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

# NOTE: These are tested in `continuous_integration/travis/test_imports.sh` If
# you modify these, make sure to change the corresponding line there.


with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

# Only include pytest-runner in setup_requires if we're invoking tests
packages = [
    'fluent', 'fluent.core', 'fluent.extensions', 'fluent.templates'
]

setup(
    name='fluent',
    version=version,
    description='',
    url='https://git.code.oa.com/yoyoyo/fluent',
    author='JOOX CMS',
    author_email='zikunchen@tencent.com',
    keywords='extract transfer load data.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 2.7",
    ],
    packages=packages,
    long_description=readme,
    python_requires=">=2.7",
    install_requires=[
        'pyyaml',
        'click',
        "psutil",
        'gevent',
        'six',
        'persistqueue',
        'apscheduler'
    ],
    tests_require=['pytest'],
    include_package_data=True,
    zip_safe=False,
    # py2不支持
    extras_require={
        "test": [
            "pytest",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "recommonmark"
        ],
    },
    # 创建命令行工具
    entry_points={"console_scripts": ["fluent = fluent.cli:main"]},
)
