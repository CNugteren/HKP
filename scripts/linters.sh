#!/usr/bin/env sh

pylint ./*.py src tests --max-line-length=120
mypy ./*.py src tests
