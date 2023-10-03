# CZ ID Platformics

* A repository that contains graphql services to manage and create workflows and entities for use with the CZ ID application. 

### Setup
To start both the `entities` and `workflows` services use
```
make init
```

### Running
After the services are running, the graphql services have endpoints at 
```
http://localhost:8008/graphql ## entities
```

```
http://localhost:8042/graphql ## workflows
```

for entities and workflows respectively

### Deployment
This project uses [happy](https://github.com/chanzuckerberg/happy/tree/main) for cloud deployment. The happy environments are defined in the [idseq-infra repo](https://github.com/chanzuckerberg/idseq-infra).

To start a stack:
1. Make sure you have happy installed. You can follow the installation instructions for happy [here](https://github.com/chanzuckerberg/happy/blob/main/docs/getting_started/installation.md).
2. Run `happy create <your-stack-name>` in the directory of the service you want to start (either `entities` or `workflows`).
3. You should be able to see the service running at `<your-stack-name>.<env>.happy.czid.org/graphql`.

For more information on happy, read their docs [here](https://github.com/chanzuckerberg/happy/tree/main/docs).

### Contributing
This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to opensource@chanzuckerberg.com.

### Reporting Security Issues
Please disclose security issues responsibly by contacting security@chanzuckerberg.com.