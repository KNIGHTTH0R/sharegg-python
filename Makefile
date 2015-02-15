all: clean build rst install

build:
	python setup.py build

dist:
	python setup.py bdist
	python setup.py sdist
	python setup.py bdist_egg

install:
	python setup.py install -f

rst:
	pandoc --from=markdown_github --to=rst README.md>README.rst

pypi: clean build dist

clean:
	rm -rf build dist sharegg.egg-info