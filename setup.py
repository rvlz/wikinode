from setuptools import setup, find_packages

with open("README.md", encoding="UTF-8") as f:
    readme = f.read()

setup(
    name="wikinode",
    version="0.2.0",
    description=(
        "A Python library that helps you " "fetch data from Wikipedia."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Ricardo Veloz",
    author_email="ricardo@rvlz.io",
    url="https://github.com/rvlz/wikinode.git",
    packages=find_packages(include=["wikinode"]),
    install_requires=["requests"],
    license="MIT license",
    keywords="wikipedia",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
