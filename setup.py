# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def get_dis():
    with open("README.markdown", "r", encoding="utf-8") as f:
        return f.read()


packages = find_packages(exclude=('test', 'tests.*', "test*"))


def main():
    version: str = "0.0.1"

    dis = get_dis()
    setup(
        name="nonebot-plugin-files",
        version=version,
        url="https://github.com/synodriver/nonebot-plugin-files",
        packages=packages,
        keywords=["asyncio", "nonebot"],
        description="async files plugin for nonebot2",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="synodriver",
        author_email="diguohuangjiajinweijun@gmail.com",
        maintainer="v-vinson",
        python_requires=">=3.6",
        install_requires=["aiohttp", "aiofiles", "typing-extensions"],
        extra_requires={"ftp": ["aioftp"], "webdav": ["aiowebdav"], "aria2": ["aioaria2"]},
        license='GPLv3',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Framework :: AsyncIO",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: Implementation :: CPython"
        ],
        include_package_data=True
    )


if __name__ == "__main__":
    main()
