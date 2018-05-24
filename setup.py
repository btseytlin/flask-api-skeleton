from os import path
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements(path.join(path.dirname(__file__), 'requirements.txt'), session='')
reqs = [str(ir.req) for ir in install_reqs]

tests_require = [
    'pytest'
]
setup(
    name='librarian',
    version='0.0.1',
    install_requires=reqs,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=tests_require,
    packages=find_packages(),
    long_description=__doc__,
    include_package_data=True,
)
