init:
	docker compose -f entities/docker-compose.yml up -d
	docker compose -f workflows/docker-compose.yml up -d
	docker compose --project-directory entities run entities alembic upgrade head
	docker compose exec --project-directory entities entities python3 scripts/seed.py
