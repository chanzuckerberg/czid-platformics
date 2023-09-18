.PHONY: gha-setup
gha-setup:
	-@docker swarm init 2>/dev/null | true
	touch .moto_recording
	docker compose up -d

.PHONY: init
init: gha-setup
	docker compose -f workflows/docker-compose.yml up -d
	$(MAKE) seed
	$(MAKE) -C entities local-init
	$(MAKE) -C workflows local-init

.PHONY: seed
seed:
	./bin/seed_moto.sh

.PHONY: clean
clean:
	docker compose -f workflows/docker-compose.yml down
	$(MAKE) -C entities local-clean
	docker compose down
	rm .moto_recording
