# KubectlBlockProcessor (v1.3) Reference

## Instruction type selector 

Processor selector: **kubectl**
Usage: **kubectl.<command>**

## Requirements

KubectlBlockProcessor generates shell commands to accomplish specific tasks using the **kubectl**
cli tool. Deploy to your kubernetes cluster by ensuring that this tool is authenticated with it's
desired target kube-apiserver.

## Main Commands

[create, delete, shell]

#### create

Create a Kubernetes resource directly from a YAML file located either locally or remotely (GET).

To create from file:

```json
{
	"type":"kubectl.create",
	"from": {
		"type":"file",
		"path":"/path/to/resource.yaml"
	}
}
```

To create remotely:

```json
{
	"type":"kubectl.create",
	"from": {
		"type":"GET",
		"url":"http://repository/path/to/resource.yaml"
	}
}
```

#### delete

Delete a Kubernetes resource directly from a YAML file located either locally or remotely (GET).

To delete from file:

```json
{
	"type":"kubectl.delete",
	"from": {
		"type":"file",
		"path":"/path/to/resource.yaml"
	}
}
```

To delete remotely:

```json
{
	"type":"kubectl.delete",
	"from": {
		"type":"GET",
		"url":"http://repository/path/to/resource.yaml"
	}
}
```

#### shell

Execute regular bash shell commands

To execute shell commands:

```json
{
	"type":"kubectl.shell",
	"cmd":"echo \"example\""
}
```

## Wait commands

[PodStatus]

#### PodStatus

Wait for a Kubernetes Pod status to read a desired state

To wait for a Pod to enter the "Running" state with a 10 second buffer:

```json
"wait_for": 
[
    	{
    		"type": "PodStatus",
    		"value": "Running",
    		"selector": "Pod",
    		"namespace": "project_name",
    		"buffer": 10
    	}
]
```

## Var commands

[ClusterIP, STDOUT, prompt]

#### ClusterIP

Grabs ClusterIP address from specified Kubernetes service resource

```json
"vars": {
    		"my-cluster-ip": 
    		{
    			"type": "ClusterIP",
    			"service": "service_name",
    			"namespace": "project_name"
    		}
}
```

#### STDOUT

Stores the contents of the last STDOUT on the current terminal session

*Note: These messages are stored dynamically in the hidden **.dolphin_last_out.log** file*

```json
"vars": {
    		"my-stdout-var": 
    		{
    			"type": "STDOUT",
    		}
}
```

#### prompt

Prompts the user for input and stores the value

```json
"vars": {
			"my-prompt-var": {
				"type":"prompt",
				"msg":"Enter a value"
			}
}
```