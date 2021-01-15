#!/usr/bin/env sh

FAILURE=0

pylint ./*.py src tests --max-line-length=120 || FAILURE=1
mypy ./*.py src tests || FAILURE=1

exit $FAILURE
