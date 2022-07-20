test:
	export VALSYS_API_BUILD=test; python login-test.py; pytest . --disable-warnings

coverage-ci:
	export VALSYS_API_BUILD=test; python login-test.py; coverage run --omit="*/test*" --source=. -m pytest . 
	
coverage:
	make coverage-ci
	coverage html
	open htmlcov/index.html

doc-gen:
	pdoc valsys -o code-docs

install:
	./scripts/install-mac.sh

tidy:
	autoflake --in-place -r .
	yapf --in-place --recursive *.py
	importanize path valsys/