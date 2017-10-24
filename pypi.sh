python setup.py clean
python setup.py sdist
twine upload dist/*
python setup.py clean
