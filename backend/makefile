dev:
	python3 src/main.py

test:
	python -m coverage run -m unittest discover src/test
	python -m coverage html
	python -m coverage report

# Build all services
.PHONY: build
build:
	@docker compose build

# Start up all services
.PHONY: up
up:
	@docker compose up -d

# Tear down all services
.PHONY: down
down:
	@docker compose down

# List the status of all services
.PHONY: ps
ps:
	@docker compose ps

# Remove all older setup and start fresh services
.PHONY: recreate
recreate: down build up ps
