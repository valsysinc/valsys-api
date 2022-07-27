test:
	export VALSYS_API_BUILD=test; python login-test.py; pytest . --disable-warnings

coverage-ci:
	export VALSYS_API_BUILD=test; python login-test.py; coverage run --omit="*/test*" --source=. -m pytest . 
	
coverage:
	make coverage-ci
	coverage html
	open htmlcov/index.html

docserver:
	mkdocs serve -a localhost:8989 --livereload

docdeploy:
	mkdocs gh-deploy 

install:
	./scripts/install-mac.sh

tidy:
	autoflake --in-place -r .
	yapf --in-place --recursive *.py
	importanize path valsys/

inttest:
	export VALSYS_API_BUILD=local; python main.py --inttests

login:
	python main.py --login

update:
	pip install -r requirements.txt