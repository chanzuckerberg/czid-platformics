# Workflows
The entities service handles secure data storage, retrieval, and basic transformations.

[YAML Schema](https://github.com/chanzuckerberg/czid-platformics/blob/main/workflows/schema/workflows.yaml) | [ER Diagram](https://github.com/chanzuckerberg/czid-platformics/tree/main/workflows/schema)


## Getting started
To run a local development environment, clone this repo and run:

```
make local-init
```

Then, visit http://localhost:8008/graphql in your favorite web browser.

To get a summary of other available `make` targets, run `make help`

### Adding or modifying entities:

- Update `schema/workflows.yaml`
- Run codegen: `make codegen`
- If changing the database:
  - Run `make alembic-autogenerate MESSAGE="reason for change goes here"`
  - Double-check that the newly generated files in `database/migrations/versions/` match your intent
  - Run `make alembic-upgrade-head` to apply migrations
- Test
- Open a PR for the updated files.
