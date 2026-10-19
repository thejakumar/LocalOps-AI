.PHONY: test backend-test frontend-test run build

backend-test:
	python -m pytest -q

frontend-test:
	cd frontend && npm test -- --run

test: backend-test frontend-test

run:
	uvicorn backend.app.main:app --reload --port 8000

build:
	docker build -t localops-ai-api .
