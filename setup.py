import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


requirements_txt = os.path.join(
    os.path.dirname(__file__),
    'requirements.txt'
)

with open(requirements_txt, 'r', encoding='utf-8') as fin:
    requires = [
        line.strip()
        for line in fin
        if line and line.strip() and not line.strip().startswith('#')
    ]

setup(
    name="fastapi-jinja",
    version="0.1.0",
    url="https://github.com/ageekinside/fastapi-jinja",
    license='MIT',

    author="Marc Brooks",
    author_email="marcwbrooks@gmail.com",

    description="Adds integration of the Jinja2 template language to FastAPI.",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),

    install_requires=requires,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
