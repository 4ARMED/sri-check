export PATH := $(PWD)/venv/bin:$(PATH)

setup:
	@python3 -m venv venv
	@pip install -r requirements.txt	
	@echo "Now run source venv/bin/activate"
