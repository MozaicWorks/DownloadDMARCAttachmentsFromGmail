.PHONY: run install dev-install lint setup.py test packager-install deb deb-install deb-remove

help: ## Print the help documentation
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Execute DownloadDMARCFilesFromGmail
	pipenv run python DownloadDMARCFilesFromGmail/download.py

install: ## Install runtime dependencies
	pipenv install --deploy

install-dev: install ## Install development dependencies
	pipenv install --deploy --dev

packager-install:
	sudo gem install fpm

setup.py:
	pipenv run pipenv-setup sync


deb: setup.py ## Create Debian package
	#fpm -s dir -t deb -n downloaddmarcfilesfromgmail --deb-no-default-config-files ./=/usr/bin

	fpm -s python -t deb --virtualenv-setup-install setup.py


deb-install: ## Install Debian package
	sudo dpkg -i ./downloaddmarcfilesfromgmail_1.0_amd64.deb


deb-remove: ## Uninstall Debian package
	sudo apt purge downloaddmarcfilesfromgmail_1.0_amd64.deb

lint: ## Check compliance with the style guide
	pipenv run flake8

test: lint ## Run unit tests
	pipenv run python -m unittest
