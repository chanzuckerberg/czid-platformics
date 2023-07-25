# Entities
The entities service handles secure data storage, retrieval, and basic transformations.


## Getting started
To run a local development environment, clone this repo and run:

```
make local-init
```

To get a summary of other available `make` targets, run `make help`

### Making changes to the DB schema:

1. Update SQLAlchemy models in `database/models`
2. Run `make alembic-autogenerate MESSAGE="reason for change goes here"`
3. Double-check that the newly generated files in `database_migrations/versions` match your intent
4. Run `make alembic-upgrade-head` to apply migrations
5. Test
6. Open a PR for the updated files.
