from setuptools import setup

setup(
    name='indexer',
    version='0.1.0',
    description='Index photos and videos',
    url='https://github.com/r1tger/indexer',
    author='Ritger Teunissen',
    author_email='github@ritger.nl',
    packages=['indexer'],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest>=3.0.0', 'freezegun'],
    install_requires=[
        'py3exiv2'
    ],
    entry_points={'console_scripts': [
        'indexer = indexer.__main__:main',
    ]},
    zip_safe=False
)
