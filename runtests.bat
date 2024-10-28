@echo off
echo Running tests...

cd tests
python -m coverage run -m unittest
python -m coverage report