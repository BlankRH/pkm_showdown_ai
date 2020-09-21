compile:
	pip3 install --upgrade pip
	python setup.py install
	yes | pyinstaller showdownai.spec || mkdir -p $(dir $@)
	cp -r teams dist/showdownai/
	zip -r dist/showdownai-linux64.zip dist/showdownai/
	cd -- "$(dirname "$BASH_SOURCE")"
	pip3 install selenium
	pip3 install --upgrade numpy
	cp chromedriver /Users/labuser/anaconda3/bin

clean:
	rm -rf build dist
