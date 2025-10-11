.PHONY: help setup run-api run-automation test clean docker-up docker-down migrate swagger

help:
	@echo "Smart Dating Optimizer - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install all dependencies (Go, Python)"
	@echo ""
	@echo "Run:"
	@echo "  make run-api        - Start Go backend API server"
	@echo "  make run-automation - Run Python automation script"
	@echo ""
	@echo "Database:"
	@echo "  make migrate-up     - Run database migrations (up)"
	@echo "  make migrate-down   - Rollback database migrations (down)"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run all tests"
	@echo "  make test-go        - Run Go tests"
	@echo "  make test-python    - Run Python tests"
	@echo "  make swagger        - Generate Swagger documentation"
	@echo "  make fmt            - Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo ""
	@echo "Clean:"
	@echo "  make clean          - Clean build artifacts"

# Setup
setup: setup-go setup-python
	@echo "Setup completed!"

setup-go:
	@echo "Installing Go dependencies..."
	go mod download
	go mod tidy

setup-python:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	playwright install

# Run
run-api:
	@echo "Starting API server..."
	go run cmd/server/main.go

run-automation:
	@echo "Running automation..."
	python main.py auto --count 10

# Database
migrate-up:
	@echo "Running migrations (up)..."
	@psql $$DATABASE_URL -f database/migrations/20251011000001_init_schema.up.sql

migrate-down:
	@echo "Running migrations (down)..."
	@psql $$DATABASE_URL -f database/migrations/20251011000001_init_schema.down.sql

# Testing
test: test-go test-python
	@echo "All tests completed!"

test-go:
	@echo "Running Go tests..."
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

test-python:
	@echo "Running Python tests..."
	pytest --cov=automations --cov=analysis --cov-report=html

# Code Quality
fmt: fmt-go fmt-python
	@echo "Code formatted!"

fmt-go:
	@echo "Formatting Go code..."
	go fmt ./...
	gofmt -s -w .

fmt-python:
	@echo "Formatting Python code..."
	black automations analysis
	isort automations analysis

lint: lint-go lint-python
	@echo "Linting completed!"

lint-go:
	@echo "Linting Go code..."
	go vet ./...

lint-python:
	@echo "Linting Python code..."
	flake8 automations analysis --max-line-length=127

# Swagger
swagger:
	@echo "Generating Swagger documentation..."
	swag init -g cmd/server/main.go -o docs/swagger

# Docker
docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

# Clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf coverage.out coverage.html
	rm -rf htmlcov .coverage
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc */*.pyc */*/*.pyc
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Clean completed!"

# Build
build-api:
	@echo "Building API server..."
	go build -o bin/server cmd/server/main.go

# Install tools
install-tools:
	@echo "Installing development tools..."
	go install github.com/swaggo/swag/cmd/swag@latest
	pip install black isort flake8 pytest pytest-cov

