.PHONY: help build build-prod run run-prod stop clean logs test

# Default target
help:
	@echo "Available commands:"
	@echo "  build      - Build development Docker image"
	@echo "  build-prod - Build production Docker image"
	@echo "  run        - Run development container"
	@echo "  run-prod   - Run production container"
	@echo "  stop       - Stop all containers"
	@echo "  clean      - Remove containers and images"
	@echo "  logs       - Show container logs"
	@echo "  test       - Test the Swagger UI"

# Build development image
build:
	docker build -f Dockerfile-dev -t swagger-ui:dev .

# Build production image
build-prod:
	docker build -f Dockerfile-prod -t swagger-ui:prod .

# Run development container
run:
	docker-compose up -d
	@echo "Swagger UI available at: http://localhost:8080"

# Run production container
run-prod: build-prod
	docker run -d \
		--name swagger-ui-prod \
		-p 8080:8080 \
		-v $(PWD)/swagger.json:/usr/share/nginx/html/swagger.json:ro \
		swagger-ui:prod
	@echo "Production Swagger UI available at: http://localhost:8080"

# Stop containers
stop:
	docker-compose down
	docker stop swagger-ui-prod 2>/dev/null || true
	docker rm swagger-ui-prod 2>/dev/null || true

# Clean up
clean: stop
	docker-compose down --rmi all --volumes --remove-orphans
	docker rmi swagger-ui:dev swagger-ui:prod 2>/dev/null || true

# Show logs
logs:
	docker-compose logs -f swagger-ui

# Test the Swagger UI
test:
	@echo "Testing Swagger UI..."
	@curl -f http://localhost:8080/health && echo "✅ Health check passed" || echo "❌ Health check failed"
	@curl -f http://localhost:8080/ > /dev/null && echo "✅ Main page accessible" || echo "❌ Main page not accessible"
	@curl -f http://localhost:8080/swagger.json > /dev/null && echo "✅ Swagger JSON accessible" || echo "❌ Swagger JSON not accessible"

# Test swagger.json loading specifically
test-swagger-load:
	@echo "Testing swagger.json loading..."
	@chmod +x test-swagger-load.sh
	@./test-swagger-load.sh

# Validate swagger.json
validate:
	@echo "Validating swagger.json..."
	@python update-spec.py --validate

# Update swagger version
update-version:
	@echo "Updating swagger version..."
	@python update-spec.py --update-version

# Update server URL
update-url:
	@echo "Usage: make update-url URL=http://localhost:5001"
	@if [ -z "$(URL)" ]; then echo "Please provide URL parameter"; exit 1; fi
	@python update-spec.py $(URL)

# Update Swagger UI to latest version
update:
	@echo "Checking for latest Swagger UI version..."
	@curl -s https://api.github.com/repos/swagger-api/swagger-ui/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | sed 's/v//'