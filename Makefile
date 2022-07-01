test:
	pytest . --disable-warnings

coverage:
	coverage run --source=. -m pytest . 
	coverage html
	open htmlcov/index.html