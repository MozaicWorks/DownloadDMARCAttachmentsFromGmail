.PHONY: run dev-install setup.py test packager-install deb deb-install deb-remove

run:
	pipenv run python DownloadDMARCFilesFromGmail/download.py


dev-install:
	pipenv install


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


test:
	pipenv run python -m unittest
