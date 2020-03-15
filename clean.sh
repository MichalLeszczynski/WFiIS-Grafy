#!/usr/bin/env bash
find . -name "*.gv" | xargs rm
find . -name "*.g" | xargs rm
find . -name "*.png" | xargs rm
find . -name "*.coverage" | xargs rm
find . -name ".pytest_cache" | xargs rm -rf
find . -name "__pycache__" | xargs rm -rf
find . -name "htmlcov" | xargs rm -rf
