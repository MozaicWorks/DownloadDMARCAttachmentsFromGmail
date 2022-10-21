run:
	pipenv run python download.py 

dev-install:
	pipenv install

test: .PHONY
	pipenv run python -m unittest

.PHONY:
