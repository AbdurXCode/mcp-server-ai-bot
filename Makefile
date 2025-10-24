# Debt Collection MCP - Development Makefile

.PHONY: help install install-dev test lint format clean run docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  clean       - Clean up temporary files"
	@echo "  run         - Run the application"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	pytest

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 .
	mypy .
	bandit -r .

format:
	black .
	isort .

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# Running the application
run:
	python run_app.py

# Docker commands
docker-build:
	docker build -t debt-collection-mcp .

docker-run:
	docker-compose up --build

docker-stop:
	docker-compose down

# Development setup
setup-dev: install-dev
	@echo "Setting up development environment..."
	cp env.example .env
	@echo "Please edit .env file with your configuration"
	@echo "Development setup complete!"

# Security checks
security:
	bandit -r .
	safety check

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Update dependencies
update-deps:
	pip-compile requirements.in
	pip-compile requirements-dev.in
