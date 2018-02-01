#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path
from os.path import join


here = path.abspath(path.dirname(__file__))

def _version():
    """ Get the local package version.
    """
    path = join("{{ cookiecutter.app_name }}", "__version__.py")
    namespace = {}
    with open(path) as stream:
        exec(stream.read(), namespace)
    return namespace["__version__"]


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the history from the HISTORY file
with open(path.join(here, 'HISTORY.md'), encoding='utf-8') as f:
    history = f.read()

try:
    import pypandoc
    long_description = pypandoc.convert_text(long_description, 'rst', format='md')
    history = pypandoc.convert_text(history, 'rst', format='md')
except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")

setup(
    name='{{ cookiecutter.app_name }}',
    version=_version(),
    description="{{ cookiecutter.app_name }}: {{ cookiecutter.app_short_description }}",
    long_description=long_description + '\n\n' + history,
    author="{{ cookiecutter.author_name }}",
    author_email='{{ cookiecutter.author_email }}',
    url="{{ cookiecutter.url }}",
    packages=["{{ cookiecutter.app_name }}"],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.cli_script }} = {{ cookiecutter.app_name }}.__main__:main'
        ]
    },
)
