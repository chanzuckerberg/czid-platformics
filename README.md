# CZ ID Platformics

* A repository that contains graphql services to manage and create workflows and entities for use with the CZ ID application. 

## Setup
To start both the `entities` and `workflows` services use
```
make init
```

Note that the Redis port of `czid-web` and `workflows` are the same, so if the initialization fails, you can stop the `czid-web` redis container and try again.


## Running
After the services are running, the graphql services have endpoints at 
```
http://localhost:8008/graphql ## entities
```

```
http://localhost:8042/graphql ## workflows
```

for entities and workflows respectively.

To generate a token for entities GQL queries:

```bash
cd entities/

# This will copy `{"Authorization": "<token>"}` to your clipboard, which you can paste into the GraphQL UI, under "Headers" at the bottom
make local-token
```


## Entities

* ER Diagram: https://github.com/chanzuckerberg/czid-platformics/tree/main/entities/schema
* YAML: https://github.com/chanzuckerberg/czid-platformics/blob/main/entities/schema/platformics.yaml

## Deployment

This project uses [happy](https://github.com/chanzuckerberg/happy/tree/main) for cloud deployment. The happy environments are defined in the [idseq-infra repo](https://github.com/chanzuckerberg/idseq-infra).

### Deploying to live environments

We have defined [GitHub Actions](https://github.com/chanzuckerberg/czid-platformics/actions) for deploying the services in each environment. To trigger these actions:
1. Select the appropriate workflow for the environment you want to deploy to (for example, [Deploy to Sandbox](https://github.com/chanzuckerberg/czid-platformics/actions/workflows/deploy-to-sandbox.yml))
2. Click `Run workflow`.
3. Select the branch you want to deploy. The default is `main`.
4. Select which service (entities or workflows) to deploy.
    * Note: When possible, it's recommended to deploy both services to ensure that changes are in sync.
5. Click the green `Run workflow` button.

### Manual deployments

**Create a new stack:**
1. Make sure you have happy installed. You can follow the installation instructions for happy [here](https://github.com/chanzuckerberg/happy/blob/main/docs/getting_started/installation.md).
2. Run `happy create <your-stack-name> -env [dev, sandbox, staging, prod]` in the directory of the service you want to start (either `entities` or `workflows`).
3. You should be able to see the service running at `<your-stack-name>.<env>.happy.czid.org/graphql`.
4. If migrations still need to be run, you can run them with `happy migrate <your-stack-name> –env [dev, sandbox, staging, prod]`.
    * If the job fails, you can also run migrations by shelling into the container with `happy shell <your-stack-name> [workflows/entities] –env [dev, sandbox, staging, prod]` and running `sh scripts/migrate.sh`.
6. If you need seed data, shell into the container with `happy shell <your-stack-name> [workflows/entities] –env [dev, sandbox, staging, prod]` then run `python3 scripts/seed.py`.
7. If you need seeded workflow versions/entities to run a workflow, shell into the container with `happy shell <your-stack-name> [workflows/entities] –env [dev, sandbox, staging, prod]` and run `python3 scripts/seed/[consensus-genome, bulk-downloads, etc]`.

**Shell into a stack:**

`happy shell <your-stack-name> [workflows/entities] –env [dev, sandbox, staging, prod]`

**Update an existing stack:**

`happy update <your-stack-name> –env [dev, sandbox, staging, prod]`

**Get logs from a stack:**

`happy logs <your-stack-name> <entities/workflows> --env [dev, sandbox, staging, prod]`

For more information on happy, read their docs [here](https://github.com/chanzuckerberg/happy/tree/main/docs).

## Contributing
This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to opensource@chanzuckerberg.com.

## Reporting Security Issues
Please disclose security issues responsibly by contacting security@chanzuckerberg.com.
