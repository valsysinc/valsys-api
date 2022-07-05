test:
	export VALSYS_API_BUILD=test; pytest . --disable-warnings

coverage:
	coverage run --source=. -m pytest . 
	coverage html
	open htmlcov/index.html