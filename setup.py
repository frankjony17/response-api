# -*- encoding: utf-8 -*-
# Source:
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'bandit',
    'flake8',
    'isort',
    'pytest'
]
unit_test_requirements = [
    'pytest',
    'pytest-cov',
    'pyyaml',
    'requests'
]
integration_test_requirements = [
    'pytest',
]
run_requirements = [
    'fastapi==0.61.1',
    'starlette==0.13.6',
    'async-exit-stack',
    'async-generator',
    'gunicorn==20.0.4',
    'uvicorn==0.11.8',
    'pydantic==1.6.1',
    'loguru==0.5.3',
    'SQLAlchemy==1.3.19',
    'psycopg2-binary==2.8.6'
]

with io.open('response_api/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="response_api",
    version=version,
    author="Frank Ricardo Ramirez",
    author_email="frankjony17@gmail.com",
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    url="https://github.com/frankjony17/response-api",
    license="COPYRIGHT",
    description="Response provider api",
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
         'dev': dev_requirements,
         'unit': unit_test_requirements,
         'integration': integration_test_requirements,
    },
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'response_api = '
            'response_api.__main__:app'
        ],
    },
)
