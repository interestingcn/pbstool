# -*- coding:utf-8 -*-
from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='pbstool',
    version='2.0',
    description='A simple-to-use program for quickly batch creating job tasks based on the PBS job scheduling system (including OpenPBS, PBS Pro, and TORQUE) based on a command list.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author=['wangzt'],
    author_email='interestingcn01@gmail.com',
    url='https://github.com/interestingcn/pbstool',
    packages=find_packages(),
    python_requires='>=3.5',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],

    install_requires=[
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'pbstool = src.__main__:fastpbs',
            'qsubs = src.__main__:qsubs'
        ]
    },
    package_data={'': ['*.cfg', '*.xml', '*.txt', '*.py']}
)