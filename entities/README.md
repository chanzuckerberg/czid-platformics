# Entities
The entities service handles secure data storage, retrieval, and basic transformations.


## Getting started
To run a local development environment, clone this repo and run:

```
make local-init
```

Then, visit http://localhost:8008/graphql in your favorite web browser.

To get a summary of other available `make` targets, run `make help`

### Making changes to the DB schema:

1. Update SQLAlchemy models in `database/models`
2. Run `make alembic-autogenerate MESSAGE="reason for change goes here"`
3. Double-check that the newly generated files in `database_migrations/versions` match your intent
4. Run `make alembic-upgrade-head` to apply migrations
5. Test
6. Open a PR for the updated files.

### Using the CLI:
```
# Get a shell in the docker container:
docker compose exec entities bash

# Get a list of samples:
./cli/gqlcli.py samples list
```
