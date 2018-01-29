all: dist

package: clean
	mkdir dist
	cp races.py dist
	pip install -r requirements.txt -t ./dist ;

dist: package
	cd dist && zip -FS -q -r racefinder.zip *

clean:
	rm -rf dist
