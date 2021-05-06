# Dolphin beta-4 Guide

In this guide, you will learn the how to create and deploy dolphin packages, work with vars, create test blocks, utilize various useful command-line options, and develop custom BlockProcessors.

## Section 1. Introduction

#### Create your first dolphin package and deploy

Getting started is quick and easy with the dolphin packager. Simply use the **create** option with the **package** command to generate a boilerplate for your project. 

Utilize dolpings package-create program to generate a new package
```bash
dolphin package-create package_name
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
dolphin deploy --file package_name/instructions.json
```

The output should be as follows (for beta-4)

```
*******************************************************
Dolphin - Cloud deployment and packaging framework.
dolphindev.com				   (beta-4)
*******************************************************
['/usr/local/bin/dolphin', 'deploy', '-f', 'package_name/instructions.json']
Gathering resources...
{'instructions_file': 'package_name/instructions.json'}
[INSTRUCTION BLOCK]************************************
Hello dolphin!
Version: beta-4
[TEST BLOCK]*******************************************
{'script': 'echo "It works!"', 'expected_result': 'It works!\n'}
PASS
{'time': 'May 06 2021 @ 10:58:07:698197 AM', 'meta': {'name': 'package_name', 'generatedBy': 'dolphin packager'}, 'id': '2ded1787ba48410281106fec7993ff43', 'tests': {0: {'script': 'echo "It works!"', 'status': 'Pass'}}, 'status': 'DeploySuccessful'}
```

#### Instruction blocks

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

Each block has a **type** you must specify the processor to use with the following convention: **<processor>.<command>**

```json
"blocks": [
    {
        "type": "kubectl.create",
        "from": {
        	"type": "GET",
        	"url": "https://<domain>/<pod_resource>.yaml",
        }
    },

    {
    	"type": "kubectl.create",
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
    	"type": "kubectl.shell",
    	"cmd": "echo \"%resource-ip%\""
    }
]
```

Block 1: Deploys a pod resource from YAML file located in a remote repository

Block 2: Waits for the pod resource to be in the "Ready" status before creating a service. After the service has been created we store the ClusterIP in our vars as resource-ip.

Block 3: Prints the resource-ip vars contents to stdout

#### Various commands

Due to additional programs such as package-create being available you must specify which program to use as the first argument
```
deploy		       dolphin deployment program
package-create	       application packaging program
```

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
-mG 			from remote manifest file retrieved with HTTP GET
--manifest-get 		from remote manifest file retrieved with HTTP GET
-mF 			from local manifest file
--manifest-file 	from local manifest file
```

Example: Deploy from a remote manifest file
```bash
dolphin deploy --manifest-get https://<domain>/manifest.json
```

You can specify just an instructions and vars files from either an HTTP GET or local the same way. It must be noted that if you do not specify vars dolphin will still utilize any preset vars in the vars.json file in the path specified in the instructions settings. If no vars are found it will be created for you at deployment time.

```
-f 			 from local instructions file
--file 			 from local instructions file
-G 			 from remote instructions file retrieved with HTTP GET
--GET 			 from remote instructions file retrieved with HTTP GET
```

To load vars you use the **preload** option to do so. There is only HTTP GET as an option for this because if a local vars.json file exists it should be loaded automatically from the directory specified in the instructions.

```
-p 			  from remote vars file retrieved with HTTP GET
--preload 		  from remote vars file retrieved with HTTP GET
```

Example: Deploy from local instructions and preload remote vars
```bash
dolphin deploy  \
--file /path_to_instructions/instructions.json \
--preload https://<domain>/vars.json
```

## Section 2. Building an instruction file

#### Settings

Set the path to your **vars** file using the settings block. If there is none dolphin will generate one for you either by using the default path **./data/vars.json** or by the specified path in **settings.varpath**

```json
"settings": {
        "varpath":"./data/"
},
```

Add a **meta** object inside of your settings block to ensure all history related to the deployment is
properly labeled.

If we wanted to note the name and version of the application deployed we would add meta labels like this:
```json
"settings": {
    ...
    "meta": {
        "name":"my application",
        "version":"1.0-beta"
    }
}
```

See the **History** section to learn more.

#### Instruction blocks

Everything is based around three simple programatic states that dolphin uses to deploy packages.

1. main cmd - create / destroy resource
2. wait for - waits for specified state to be returned from cloud API
3. vars - store values from cloud API dynamically

When developing a custom block processor all functions should return back to the parser these three things in the order of: (main_cmd, var_cmd, wait_for)

#### Test blocks

Built into dolphin is a very simple automated sanity test instruction block. In the beta version this can not be customized; however, you can add tests to your own custom block processor module in place of this.

Use the **script** key along with a shell script value along with the **expected_result** key with the plain text output you expect. The STDOUT from the script will be matched against your expected result and determine a PASS/FAIL

Simple test blocks that match an echo script's STDOUT to an expected result.

```json
"tests": [

        {
            "script":"echo \"test\"",
            "expected_result":"test\n"
        },

        {
            "script":"echo \"test1\"",
            "expected_result":"test1\n"
        },

        {
            "script":"echo \"test2\"",
            "expected_result":"test2\n"
        }
    ]
```

Output

```
[TEST BLOCK]*******************************************
{'script': 'echo "test"', 'expected_result': 'test\n'}
PASS
[TEST BLOCK]*******************************************
{'script': 'echo "test1"', 'expected_result': 'test1\n'}
PASS
[TEST BLOCK]*******************************************
{'script': 'echo "test2"', 'expected_result': 'test2\n'}
PASS
```

## Section 3. History

#### History fingerprints

Every deployment and test that is run with dolphin produces a **fingerprint** which contains both generated and user defined data.

Example of a fingerprint:
```json
{
    "time": "May 06 2021 @ 10:58:07:698197 AM", 
    "meta": {
        "name": "package_name", 
	"generatedBy": "dolphin packager"
    }, 
    "id": "2ded1787ba48410281106fec7993ff43", 
    "tests": {
        0: {
	    "script": "echo "It works!"", 
	    "status": "Pass"
	   }
    }, 
    "status": "DeploySuccessful"
}
```

The generated fields **time**, **id**, **status**, and all **test** fields are managed by dolphin. Anything in the **meta** section is user defined and is a direct copy of what was input in the meta object within the settings block of the deployed instructions.

#### Showing & searching history

You utilize the **history** application with dolphin to print history to the terminal and easily search history using labels.

To show all history:
```bash
dolphin history
```

To search for a specific label use the **-l** option to search for fingerprints with specified labels.

**Note:** Encapsulate your each label with single or double quotes after the -l option

To search for a single label:
```bash
dolphin history -l 'version:1.0'
```

To search for multiple labels:
```bash
dolphin history -l 'version:1.0' 'name:myApp' 'cluster:myKubernetesCluster'
```
