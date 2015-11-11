.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "authors - update list of authors"
	@echo "test - run tests for current version of python"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr venv_temp/
	find . -name '*.egg-info' -not -path '*venv_18*' -exec rm -fr {} +
	find . -name '*.egg' -not -path '*venv_18*' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

release: clean
	python setup.py sdist upload

dist: clean
	python setup.py sdist
	ls -l dist

install: clean
	python setup.py install

authors:
	git log --format='%aN <%aE>' | sort -u | cat > AUTHORS.rst

test:
	python runtests.py
