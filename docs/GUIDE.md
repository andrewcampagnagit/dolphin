# Dolphin Beta-3 Guide

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
dolphin deploy --file /package_name/instructions.json
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

The settings section is where you can select the processor **mode** and describe your desired **varpath**. This section can also be used to store metadata about the deployment or objects to be used with custom block processor modules.

In this example we have selected **kubectl** mode to tell dolphin to deploy using the **kubectlblock** processor.

```json
"settings": {
        "mode":"kubectl",
        "varpath":"./data/"
},
```

For development the **mode** is value is used in the **instructionparser.py**

```python
if mode == "kubectl":
    self.processor = lambda block: kubectlblock.processblock(block)
```

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



