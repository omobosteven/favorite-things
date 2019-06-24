from setuptools import setup, find_packages

setup(
    name='favorite_things',
    version='1.0',
    scripts=['manage.py'],
    author='Stephen Omobo',
    author_email='stephen.omobo@gmail.com',
    description='A module to track favorite things',
    url='https://github.com/omobosteven/favorite-things',
    packages=find_packages(),
)
