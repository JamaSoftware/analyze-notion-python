from setuptools import setup, find_packages
setup(
    name='notion-python',
    version='1.0.0',
    description='API Client for Notion',
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
