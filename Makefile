setup:
	chmod +x ./setup.sh &&\
		./setup.sh

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black .

lint:
	find src -type f -name "*.py" -print0 | xargs -0 pylint

precommit:
	pre-commit install
	pre-commit run --all-files

refactor: format precommit lint

m ?= "Quick commit"
push:
	git add . && git commit -m $(m) && git push

docker:
	docker-compose up -d --build

run:
	python src/main.py

.PHONY: setup install format lint precommit refactor push docker run
