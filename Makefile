.PHONY: run install dev-install lint tag setup.py test packager-install deb deb-install deb-remove

help: ## Print the help documentation
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Cleans the distribution directory
	rm -rf ./dist ./build ./*.egg-info

run: ## Execute DownloadDMARCFilesFromGmail
	pipenv run python -m DownloadDMARCFilesFromGmail $(args)

install: ## Install runtime dependencies
	pipenv install --deploy

install-dev: install ## Install development dependencies
	pipenv install --deploy --dev

install-build: ## Install build dependencies
	pipenv install --deploy --categories="build"

format: ## Format source and test code according to PEP8 standards
	pipenv run black --skip-string-normalization DownloadDMARCFilesFromGmail tests

lint: ## Check compliance with the style guide
	pipenv run flake8 DownloadDMARCFilesFromGmail tests

test: lint ## Run unit tests
	pipenv run python -m unittest

packager-install:
	sudo gem install fpm

setup.py: ## Sync dependencies in Pipfile or Pipfile.lock to setup.py
	pipenv run pipenv-setup sync


deb: setup.py ## Create Debian package
	#fpm -s dir -t deb -n downloaddmarcfilesfromgmail --deb-no-default-config-files ./=/usr/bin

	fpm -s python -t deb --virtualenv-setup-install setup.py


deb-install: ## Install Debian package
	sudo dpkg -i ./downloaddmarcfilesfromgmail_1.0_amd64.deb


deb-remove: ## Uninstall Debian package
	sudo apt purge downloaddmarcfilesfromgmail_1.0_amd64.deb

dist: clean ## Creates a source distribution and wheel distribution
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine check ./dist/*
	pipenv run check-wheel-contents dist/*.whl

tag: ## Tag version
	if [[ -z "${version}" ]]; then echo "version must be set";false; fi
	git tag -a $(version) -m "Bump version $(version)"
	git push origin master --follow-tags
