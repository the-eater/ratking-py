from setuptools import setup

setup(
    name="ratking",
    version="v1.0",
    description="An all purpose package manager",
    author="eater.",
    author_email="python@eater.me",
    url="https://github.com/the-eater/ratking-py",
    py_modules=['ratkings'],

    entry_points={
        'console_scripts': ['rk=ratking'],
    },
    install_requires=[
        'toml',
        'docopt'
    ],
    include_package_data=True,
    license='MIT',
)