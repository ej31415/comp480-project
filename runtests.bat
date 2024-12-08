@echo off
echo Running tests...

cd tests
python -m coverage run -m unittest -v
python -m coverage report
python -m coverage html