pip cache purge

rm -rf dist
rm -rf build

pip install wheel twine

python setup.py sdist
python setup.py bdist_wheel

twine upload --repository-url https://pypi.org/legacy/ dist/*.whl --verbose

pypi-AgEIcHlwaS5vcmcCJDhmYTRkYzVjLTg1NDMtNGMwZi1iNWNjLTc0YWZhMTZmNjNmYgACKlszLCI3MDM1MjdiMC0wNDExLTQ3M2YtOGEzNy01YjQ0OTMxMjQyMzciXQAABiAvbhjM6JIjOFMoyjNMefgK5d3jDWwQ-LfzISXWL7GJ2Q