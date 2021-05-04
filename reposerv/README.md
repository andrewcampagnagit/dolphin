# dolphin reposerv (In development)

[![Generic badge](https://img.shields.io/badge/python-3.7-blue)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/dolphin-reposerv--v1.0-orange)](https://shields.io)

#### Summary

Start up dolphin reposerv API on virtual machine or in a container to host all of your dolphin packages locally for enterprise, private use, or public repository service. In addition you can call the reposerv back with deployment 
and test information to help manage application deployments accross multiple machines. You can connect several reposerv
instances together to create a highly available cluster.

#### Whats new?

- Repository API: Host manifest and resource files locally
- Security: Authentication enabled for simple JWT based login for API communication
- Callback: Send test results, deployment metadata, and version information back to reposerv
- Clustering: Multiple reposerv instances can be used to provide HA