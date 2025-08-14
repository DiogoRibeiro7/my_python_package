.PHONY: help install format lint type-check test test-cov clean build publish-test publish setup dev-install security docs tox

help:
	@echo "Available commands:"
	@echo "  make install      Install the package and dependencies"
	@echo "  make dev-install  Install the package and dev dependencies"
	@echo "  make setup        Install pre-commit hooks and dev dependencies"
	@echo "  make format       Format code with black, isort, and ruff"
	@echo "  make lint         Lint code with ruff"
	@echo "  make type-check   Type check with mypy"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo "  make tox          Run tests in multiple Python environments"
	@echo "  make security     Run security checks with bandit"
	@echo "  make docs         Generate documentation"
	@echo "  make clean        Remove build artifacts"
	@echo "  make build        Build package"
	@echo "  make publish-test Publish to TestPyPI"
	@echo "  make publish      Publish to PyPI"

install:
	poetry install --no-dev

dev-install:
	poetry install

setup:
	poetry install
	pre-commit install

format:
	poetry run black src tests
	poetry run isort src tests
	poetry run ruff format src tests

lint:
	poetry run ruff check src tests

type-check:
	poetry run mypy src tests

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=my_python_package --cov-report=term-missing

tox:
	poetry run tox

security:
	poetry run bandit -r src/

docs:
	poetry run python scripts/generate_docs.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	poetry build

publish-test: build
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

publish: build
	poetry publish

check-deps:
	python scripts/check_imports_vs_pyproject.py --fix --resolve-latest --strategy caret

bump-patch:
	python scripts/pyproject_editor.py bump-version patch

bump-minor:
	python scripts/pyproject_editor.py bump-version minor

bump-major:
	python scripts/pyproject_editor.py bump-version major
