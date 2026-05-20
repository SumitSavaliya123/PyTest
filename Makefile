.PHONY: install test smoke crud schema negative coverage clean help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run full test suite"
	@echo "  make smoke      - Run smoke tests only"
	@echo "  make crud       - Run CRUD tests only"
	@echo "  make schema     - Run schema validation tests only"
	@echo "  make negative   - Run negative tests only"
	@echo "  make posts      - Run posts tests only"
	@echo "  make users      - Run users tests only"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make clean      - Remove reports and cache"

install:
	pip install -r requirements.txt

test:
	pytest -v

smoke:
	pytest -m smoke -v

crud:
	pytest -m crud -v

schema:
	pytest -m schema -v

negative:
	pytest -m negative -v

posts:
	pytest -m posts -v

users:
	pytest -m users -v

coverage:
	pytest --cov=tests --cov-report=html:reports/coverage --cov-report=term-missing

parallel:
	pytest -n auto -v

clean:
	rm -rf reports/ .pytest_cache/ __pycache__/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
