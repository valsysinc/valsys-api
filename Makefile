test:
	export VALSYS_API_BUILD=test; pytest . --disable-warnings

coverage:
	coverage run --source=. -m pytest . 
	coverage html
	open htmlcov/index.html

doc-gen:
	pdoc valsys -o docs

install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	cp env/.env env/.env.bak
	cp env/.env.test env/.env