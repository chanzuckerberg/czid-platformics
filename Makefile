init:
	docker compose -f entities/docker-compose.yml up -d
	docker compose -f workflows/docker-compose.yml up -d
	$(MAKE) -C entities local-init
