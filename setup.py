from os import path

from setuptools import setup

EXTRAS_REQUIRE = {
    "tests": ["pytest", "pytest-cov", "pytest-mock"],
    "lint": [
        "isort",
        "black",
        "flake8",
        "flake8-bugbear",
        "flake8-builtins",
        "mypy",
        "docformatter",
        "pre-commit",
    ],
    "tools": ["codecov", "bump2version"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + EXTRAS_REQUIRE["tools"]


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding="utf-8") as f:
        return f.read()


setup(
    name="cosmospy",
    version="3.0.2",  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT
    author="hukkinj1",
    author_email="hukkinj1@users.noreply.github.com",
    description="Tools for Cosmos wallet management and offline transaction signing",
    url="https://github.com/hukkinj1/cosmospy",
    project_urls={"Changelog": "https://github.com/hukkinj1/cosmospy/blob/master/CHANGELOG.md"},
    packages=["cosmospy"],
    package_data={"cosmospy": ["py.typed"]},
    zip_safe=False,  # For mypy to be able to find the installed package
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=[
        "ecdsa>=0.14.0,<0.16.0",
        "bech32>=1.1.0,<2.0.0",
        "typing-extensions>=3.7.4,<4.0.0; python_version<'3.8'",
    ],
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.6",
    keywords="cosmos blockchain atom cryptocurrency",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)
