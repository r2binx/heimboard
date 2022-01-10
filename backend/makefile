dev:
	python3 src/main.py

build:
	pyinstaller heimboard-backend.spec

clean:
	rm -rf build dist
	find . -type d -name __pycache__ -exec rm -r {} \+
	
deps:
	pip3 install -r requirements.txt