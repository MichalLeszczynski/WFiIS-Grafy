#!/usr/bin/env bash

# Generate code & branch coverage report
coverage run --source=../ --branch -m pytest
coverage html
google-chrome htmlcov/index.html &
