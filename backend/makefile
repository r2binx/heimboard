dev:
	python3 main.py

build:
	pyinstaller heimboard-backend.spec

build-wakeup:
	pyinstaller wakeup.spec

clean:
	rm -rf build dist
	find . -type d -name __pycache__ -exec rm -r {} \+
	
deps:
	pip3 install -r requirements.txt