MAKEFLAGS += --jobs=2

.PHONY: gha-setup
gha-setup:
	-@docker swarm init 2>/dev/null | true
	touch .moto_recording
	docker compose up -d

.PHONY: init
init: rebuild gha-setup
	$(MAKE) seed
	$(MAKE) -C entities local-init
	$(MAKE) -C workflows local-init

.PHONY: seed
seed:
	./bin/seed_moto.sh

.PHONY: rebuild
rebuild: rebuild-entities rebuild-workflows
	
rebuild-workflows:
	$(MAKE) -C workflows local-rebuild

rebuild-entities:
	$(MAKE) -C entities local-rebuild

.PHONY: clean
clean:
	$(MAKE) -C entities local-clean
	$(MAKE) -C workflows local-clean
	docker compose down
	rm -rf .moto_recording
