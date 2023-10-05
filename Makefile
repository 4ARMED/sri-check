export PATH := $(PWD)/venv/bin:$(PATH)

setup:
	@python3 -m venv venv
	@pip install -r requirements.txt	
	@echo "Now run source venv/bin/activate"

build:
	@python -m build

upload: build
	@python -m twine upload --repository sri-check dist/*