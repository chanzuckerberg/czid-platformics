init:
	docker compose up -d
	docker compose run entities alembic upgrade head
	docker compose exec entities python3 scripts/seed.py
