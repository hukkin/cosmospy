from os import path
from setuptools import setup


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding='utf-8') as f:
        return f.read()


setup(
    name='cosmospy',
    version='0.0.0',  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT
    author='hukkinj1',
    author_email='hukkinj1@users.noreply.github.com',
    description='Cosmos utilities',
    url='https://github.com/hukkinj1/cosmospy',
    packages=['cosmospy'],
    package_data={'cosmospy': ['py.typed']},
    zip_safe=False,  # For mypy to be able to find the installed package
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['secp256k1==0.13.2'],
    python_requires='>=3.6',
    classifiers=['Typing :: Typed'],
)
