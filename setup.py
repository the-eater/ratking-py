from setuptools import setup

setup(
    name="ratking",
    version="v1.0",
    description="An all purpose package manager",
    author="eater.",
    author_email="python@eater.me",
    url="https://github.com/the-eater/ratking-py",
    packages=[
        'ratking',
        'ratking.repository',
        'ratking.dist_object',
        'ratking.version_selector'
    ],

    entry_points={
        'console_scripts': ['rk=ratking:main'],
    },
    install_requires=[
        'toml',
        'docopt',
        'tatsu'
    ],
    include_package_data=True,
    license='MIT',
)