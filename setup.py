#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "verif",

    version = "0.1.1",
    author = "Jinhuan Zhu",
    author_email = "jinhuanzhu@seniverse.com",
    url=" http://git.thinkpage.cn/camellia/camellia-verification",

    description="forecast verification.",

    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        "pandas",
        "matplotlib",
        "numpy"
    ]
)
