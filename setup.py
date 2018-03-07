from setuptools import setup, find_packages
setup(
    name='notion-python',
    version='1.0.0',
    description='API Client for Notion',
    keywords='notion api client',
    packages=find_packages(),
    install_requires=['requests'],
)
