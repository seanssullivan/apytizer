docs:
	python setup.py build_sphinx

bdist_wheel:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	pytest --cov-report html:htmlcov --cov=src tests --tb=short

tox:
	tox
