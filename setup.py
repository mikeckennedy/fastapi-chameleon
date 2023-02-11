import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


def read_version():
    filename = os.path.join(os.path.dirname(__file__), 'fastapi_chameleon', '__init__.py')
    with open(filename, mode="r", encoding='utf-8') as fin:
        for line in fin:
            if line and line.strip() and line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'").strip('"')

    return "0.0.0.0"


# requirements_txt = os.path.join(
#      os.path.dirname(__file__),
#     'requirements.txt'
# )

# with open(requirements_txt, 'r', encoding='utf-8') as fin:
#     requires = [
#         line.strip()
#         for line in fin
#         if line and line.strip() and not line.strip().startswith('#')
#     ]

requires = ["fastapi", "Chameleon"]

setup(
    name="fastapi_chameleon",
    version=read_version(),
    url="https://github.com/mikeckennedy/fastapi-chameleon",
    license='MIT',

    author="Michael Kennedy",
    author_email="michael@talkpython.fm",

    description="Adds integration of the Chameleon template language to FastAPI.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests', 'example', 'readme_resources', 'build', 'dist',)),

    install_requires=requires,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
