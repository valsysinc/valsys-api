test:
	export VALSYS_API_BUILD=test; python login-test.py; pytest . --disable-warnings

coverage-ci:
	rm -f coverage.svg
	export VALSYS_API_BUILD=test; python login-test.py; coverage run  --source=. -m pytest . 
	coverage-badge -o coverage.svg

coverage:
	make coverage-ci
	coverage html
	open htmlcov/index.html
	coverage-lcov
	
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
	python main.py --inttests

login:
	python main.py --login

update:
	pip install -r requirements.txt

deploy:
	git push github master
	make docdeploy