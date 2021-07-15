# _*_ coding: utf-8 _*_
import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    desc = f.read()


setuptools.setup(
    name='abnormalities',
    version='1.0.1',
    author='Kris Liang',
    author_email='criselyj@163.com',
    description='patch all exception functions.',
    url='https://github.com/Kr1s77/abnormalities/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)