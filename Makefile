all: clean build install

build:
	python setup.py build

dist:
	python setup.py bdist
	python setup.py sdist
	python setup.py bdist_egg

install:
	python setup.py install -f

pypi: clean build dist

clean:
	rm -rf build dist sharegg.egg-info