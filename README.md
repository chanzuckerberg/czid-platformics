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

### Contributing
This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to opensource@chanzuckerberg.com.

### Reporting Security Issues
Please disclose security issues responsibly by contacting security@chanzuckerberg.com.