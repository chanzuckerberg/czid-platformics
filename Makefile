.PHONY: gha-setup
gha-setup:
	-@docker swarm init 2>/dev/null | true
	docker compose up -d

.PHONY: init
init: gha-setup
	$(MAKE) -C entities local-init
	$(MAKE) -C workflows local-init

.PHONY: clean
clean:
	$(MAKE) -C entities local-clean
	$(MAKE) -C workflows local-clean
	docker compose down
