from setuptools import setup, find_packages
from os.path import realpath, dirname, join

def long_description():
    readme_path = join(dirname(realpath(__file__)), 'README.rst')
    with open(readme_path) as readme:
        return readme.read()

setup(
    name='notion-python',
    version='1.0.1',
    description='API Client for Notion',
    long_description=long_description(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='notion api client',
    project_urls={
        'Source': 'https://github.com/notion-data/notion-python',
    },
    packages=find_packages(),
    install_requires=['requests'],
)
