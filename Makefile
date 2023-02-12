.PHONY: run install dev-install lint setup.py test packager-install deb deb-install deb-remove

run:
	pipenv run python DownloadDMARCFilesFromGmail/download.py


install:
	pipenv install --deploy

install-dev:
	pipenv install --deploy --dev

packager-install:
	sudo gem install fpm


setup.py:
	pipenv run pipenv-setup sync


deb: setup.py
	#fpm -s dir -t deb -n downloaddmarcfilesfromgmail --deb-no-default-config-files ./=/usr/bin

	fpm -s python -t deb --virtualenv-setup-install setup.py


deb-install:
	sudo dpkg -i ./downloaddmarcfilesfromgmail_1.0_amd64.deb


deb-remove:
	sudo apt purge downloaddmarcfilesfromgmail_1.0_amd64.deb


lint:
	pipenv run flake8

test: lint
	pipenv run python -m unittest
