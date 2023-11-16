# Entities
The entities service handles secure data storage, retrieval, and basic transformations.

[YAML Schema](https://github.com/chanzuckerberg/czid-platformics/blob/main/entities/schema/platformics.yaml) | [ER Diagram](https://github.com/chanzuckerberg/czid-platformics/tree/main/entities/schema)


## Getting started
To run a local development environment, clone this repo and run:

```
make local-init
```

Then, visit http://localhost:8008/graphql in your favorite web browser.

To get a summary of other available `make` targets, run `make help`

### Adding or modifying entities:

- Update `schema/platformics.yaml`
- Run codegen: `make codegen`
- If changing the database:
  - Run `make alembic-autogenerate MESSAGE="reason for change goes here"`
  - Double-check that the newly generated files in `database_migrations/versions` match your intent
  - Run `make alembic-upgrade-head` to apply migrations
- Test
- Open a PR for the updated files.

### Using the CLI:
```
# Get a shell in the docker container:
docker compose exec entities bash

# Get a list of samples:
export PLATFORMICS_AUTH_TOKEN=$(./platformics/cli/generate_token.py auth generate-token 111 --project 444:admin --expiration 3600)
./cli/gqlcli.py samples list
```

### Debugging in VSCode:
- Install the 'Dev Containers' and 'Docker' VSCode extensions
- Open VSCode at the entities directory
- Click "reopen in container" when VSCode suggests it.
- You're now editing code directly in the container! This is handy because all of the python packages used by the app are installed in the container and type checking will work properly.
- You can set breakpoints and click the "debug/play" icon in VSCode to step through your code. 
  - **Note** that you'll generally have to make a request (via cli/browser/???) to actually trigger the section of code you're debugging.
