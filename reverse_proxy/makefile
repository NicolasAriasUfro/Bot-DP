
# Build all services
.PHONY: build
build:
	@docker-compose build

# Start up all services
.PHONY: up
up:
	@docker-compose up -d

# Tear down all services
.PHONY: down
down:
	@docker-compose down

# Remove all older setup and start fresh services
.PHONY: recreateJ
recreate: down build up
