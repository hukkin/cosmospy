#!/usr/bin/env bash
# Remember to `git checkout <tag>` to the correct branch before running this script!
python3 setup.py sdist \
&& pip3 install --upgrade twine \
&& twine check dist/* \
&& twine upload dist/*
