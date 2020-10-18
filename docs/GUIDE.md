# Dolphin Beta-3 Guide

In this guide, you will learn the how to create and deploy dolphin packages, work with vars, create test blocks, utilize various useful command-line options, and develop custom BlockProcessors.

## Architecture

## Create your first dolphin package and deploy

Getting started is quick and easy with the dolphin packager. Simply use the **create** option with the **package** command to generate a boilerplate for your project. 

```bash
podman run dolphin package create <package_name>
```

You should see a structure like this created

```
.
└── package_name
    ├── data
    │   └── vars.json
    └── instructions.json
```

The instructions and vars created for you will contain a simple deployment setup. You can deploy from file by using the **deploy** command.

```bash
podman run -v $(pwd)/package_name:/package_name \
dolphin:latest deploy \
--file /package_name/instructions.json
```

The output should be as follows (for beta-3)

```
*******************************************************
Dolphin - Cloud deployment and packaging framework.
dolphindev.com				   (beta-3)
*******************************************************
Gathering resources...
[INSTRUCTION BLOCK]************************************
Hello dolphin!
Version: beta-3
*******************************************************
instructions=1 tests=0
[CLEAN UP]*********************************************
Done!
```

## Instruction blocks

The instruction blocks can be found in this section of the instructions file

```json
"blocks": [
    {
        ...
    }
]
```

An instruction block contains a **main command** and can also contain a **wait for** and **vars** command. Together these three types of commands allow you to tell dolphin exactly what to do at each step or **instruction block** of your deployment.

Out of the box dolphin comes with the kubectlblock **BlockProcessor** and it contains various commands we can use to strategize our cloud application deployment. Take for example the following blocks.

```json
"blocks": [
    {
        "type": "create",
        "from": {
        	"type": "GET",
        	"url": "https://<domain>/<pod_resource>.yaml",
        }
    },

    {
    	"type": "create",
    	"from": {
    		"type": "GET",
    		"url": "https://<domain>/<service_resource>.yaml"
    	},

    	"vars": {
    		"resource-ip": {
    			"type": "ClusterIP",
    			"service": "service_name",
    			"namespace": "project_name"
    		}
    	},

    	"wait_for": [
    		{
    			"type": "PodStatus",
    			"selector": "Ready",
    			"namespace": "project_name"
    		}
    	]
    },

    {
    	"type": "shell",
    	"cmd": "echo \"%resource-ip\""
    }
]
```

Block 1: Deploys a pod resource from YAML file located in a remote repository

Block 2: Waits for the pod resource to be in the "Ready" status before creating a service. After the service has been created we store the ClusterIP in our vars as resource-ip.

Block 3: Prints the resource-ip vars contents to stdout

## Various commands

There are several ways you can configure your deployment package for both local and remote use. Both the out of the box kubectlblock processor and dolphin itself comes with a way to download remote resources using simple HTTP GET requests. You can condense your deployment down to a single **manifest** file for easy distribution. Below is an example manifest file.

```json
{
	"instructions_url":"https://<domain>/instructions.json",
	"var_url":"https://<domain>/vars.json"
}
```

This file can be used with the manifest options to retrieve both instructions and preset vars for deployment. When you couple this with the kubectlblock processors from type GET option you can have a true remote deployment of cloud resources.

For manifest file deployments use the following options:

```
-mG 				from remote manifest file retrieved with HTTP GET
--manifest-get 		from remote manifest file retrieved with HTTP GET
-mF 				from local manifest file
--manifest-file 	from local manifest file
```

Example: Deploy from a remote manifest file
```bash
podman run dolphin:latest deploy \
--manifest-get https://<domain>/manifest.json
```

You can specify just an instructions and vars files from either an HTTP GET or local the same way. It must be noted that if you do not specify vars dolphin will still utilize any preset vars in the vars.json file in the path specified in the instructions settings. If no vars are found it will be created for you at deployment time.

```
-f 					from local instructions file
--file 				from local instructions file
-G 					from remote instructions file retrieved with HTTP GET
--GET 				from remote instructions file retrieved with HTTP GET
```

To load vars you use the **preload** option to do so. There is only HTTP GET as an option for this because if a local vars.json file exists it should be loaded automatically from the directory specified in the instructions.

```
-p 					from remote vars file retrieved with HTTP GET
--preload 			from remote vars file retrieved with HTTP GET
```

Example: Deploy from local instructions and preload remote vars
```bash
podman run -v /path_to_instructions:/path_to_instructions dolphin:latest deploy \
--file /path_to_instructions/instructions.json \
--preload https://<domain>/vars.json
```


