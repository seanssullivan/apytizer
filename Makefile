docs:
	python setup.py build_sphinx

build:
	hatch build

test:
	pytest --cov-report html:htmlcov --cov=src tests --tb=short

tox:
	tox -- tests/$(path)
