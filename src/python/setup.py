__author__ = 'GCC'
from setuptools import setup, find_packages

# To build for local development use 'python setup.py develop'.
# To upload a version to pypi use 'python setup.py clean sdist upload'.
# Docs are built with 'make html' in the docs directory parallel to this one
setup(
    name='bt_joystick',
    version='1.0.0',
    description='',
    classifiers=['Programming Language :: Python :: 3.5'],
    url='https://github.com/GamesCreatorsClub/GCC-Joystick/',
    author='Daniel Sendula, Pal Denes',
    author_email='bt_joystick@mail-list-of-some-kind',
    license='MIT',
    packages=find_packages(),
    # install_requires=['evdev==1.1.2'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    dependency_links=[],
    zip_safe=False)
