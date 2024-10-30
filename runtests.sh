#!/bin/bash
echo "Running tests..."

cd tests
python3 -m coverage run -m unittest -v
python3 -m coverage report