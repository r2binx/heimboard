hidden_imports = --hidden-import uvicorn --hidden-import uvicorn.logging --hidden-import uvicorn.loops --hidden-import uvicorn.loops.auto --hidden-import uvicorn.protocols --hidden-import uvicorn.protocols.http --hidden-import uvicorn.protocols.http.auto --hidden-import uvicorn.protocols.websockets --hidden-import uvicorn.protocols.websockets.auto --hidden-import uvicorn.lifespan --hidden-import uvicorn.lifespan.on
arch = $(shell uname -m)

dev:
	python3 main.py reload

dev-wakeup:
	python3 src/wakeup.py reload

build:
	pyinstaller --onefile $(hidden_imports) \
		--hidden-import main \
		-n "heimboard-backend.linux-$(arch)" \
		main.py

build-wakeup:
	pyinstaller --onefile $(hidden_imports) \
		--hidden-import wakeup \
		-n "wakeup.linux-$(arch)" \
		src/wakeup.py

clean:
	rm -rf build dist *.spec
	find . -type d -name __pycache__ -exec rm -r {} \+
	
deps:
	pip3 install -r requirements.txt
