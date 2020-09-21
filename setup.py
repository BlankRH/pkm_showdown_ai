import os
from setuptools import setup, find_packages
#from pip._internal.req import parse_requirements
import uuid


REQUIRED_PACKAGES = [
    'beautifulsoup4',
    'Flask',
    'itsdangerous',
    'Jinja2',
    'MarkupSafe',
    'path.py',
    'PyInstaller',
    'requests',
    'selenium',
    'webargs',
    'Werkzeug',
]

setup(
    name = "showdownai",
    version = "1.0.1",
    author = "Vasu Vikram",
    author_email = "vasumvikram@gmail.com",
    description = "",
    license = "MIT",
    keywords = "",
    url = "",
    packages=find_packages(include=[
        'showdownai',
        'smogon',
        'server',
        'pokemonitor'
    ]),
    include_package_data=True,
    package_data={
        'static': 'server/static/*',
        'templates': 'server/templates/*'
    },
    entry_points={
        'console_scripts': [
            'showdownai=showdownai.showdown:main',
            'simulator=showdownai.game:main',
            'showdownmonitor=pokemonitor.__init__:main',
            'multitest=showdownai.multitest:run',
            'showdownserver=server.server:main'
        ],

    },
    install_requires=REQUIRED_PACKAGES,
    long_description="",
    classifiers=[
    ],
)
