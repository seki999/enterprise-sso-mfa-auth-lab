.PHONY: setup up down seed test screenshots backend frontend

setup:
	cd backend && python -m pip install -r requirements.txt
	cd frontend && npm install

up:
	docker compose up --build

down:
	docker compose down

seed:
	cd backend && python -m app.seed

test:
	cd backend && pytest

screenshots:
	cd frontend && npm run screenshots

backend:
	cd backend && python -m uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev
