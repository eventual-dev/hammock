#!/bin/sh -e

export SOURCE_FILES="hammock tests"
set -x

autoflake --in-place --recursive $SOURCE_FILES
isort --project=hammock $SOURCE_FILES
black $SOURCE_FILES
