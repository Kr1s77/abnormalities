# _*_ coding: utf-8 _*_
import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    desc = f.read()


setuptools.setup(
    name='abnormalities',
    version='1.0',
    author='Kris Liang',
    author_email='criselyj@163.com',
    description='patch all exception functions.',
    url='https://github.com/Kr1s77/tracer/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)