APP = $(notdir $(CURDIR))
TAG = $(shell echo "$$(date +%F)-$$(git rev-parse --short HEAD)")
DOCKER_REPO = ghcr.io/managedkaos


help:
	@echo "Run make <target> where target is one of the following..."
	@echo
	@echo "    requirements - install required libraries"
	@echo "    lint         - run flake8 and pylint"
	@echo "    build        - build docker container"
	@echo "    clean        - stop local container, clean up workspace"

requirements:
	pip install --upgrade pip

	pip install --quiet --upgrade \
		--requirement development-requirements.txt

	pip install --quiet --upgrade \
		--requirement requirements.txt

lint:
	flake8 --ignore=E501,E231 *.py
	pylint --errors-only --disable=C0301 *.py
	black --diff *.py
	isort --check *.py

black:
	black *.py

isort:
	isort *.py

test:
	python -m unittest --verbose --failfast

build: pip lint
	docker build --tag $(APP):$(TAG) .

clean:
	docker container stop $(APP) || true
	docker container rm $(APP) || true
	@rm -rf ./__pycache__ ./tests/__pycache__
	@rm -f .*~ *.pyc

run:
	./run.sh

.PHONY: build clean deploy help interactive lint pip run test unittest upload
