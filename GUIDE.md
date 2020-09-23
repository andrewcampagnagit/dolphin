# How to use dolphin (beta-2)

## Getting started

To get started we will use the pre-built example deployment that
comes with the dolphin package. We will use the **deploy** option
to tell dolphin this is a deployment.
```bash
python3 app/dolphin.py deploy qa/instructions_1_qa.json
```

You should recieve the output indicating that dolphin is ready for use.
```
Dolphin version beta-2
Created by Server Center - Cloud Development Software
```

## Blocks and stages

Each deployment has an instruction file which you specify in the command
line. This file can be local or hosted and contains three types of **blocks**.

**Settings block**\
Every instruction file should have a settings block. This specifies mode
and location of variables.

```json
...
"settings": {
		"mode":"kubectl",
		"varpath":"./data/"
	}
...
```

**Instruction blocks**\
Multiple instruction blocks make up a deployment and when processed are refered
to as stage which are the raw shell commands that actually do the resource
creation.

```json
...
"blocks": [
		
		{
			"type":"shell",
			"cmd":"echo \"Hello world!\""
		}

	]
...
```

**Metadata block**\
As implied by the name this block contains whatever JSON object you want and it
will be ignored by the processor

```json
...
"meta": {
		"name":"Beta development instruction template",
		"version":{
			"dolphin":"beta-2",
			"template":"2.0"
		},
		"author":"Andrew Campagna"
	}
...
```

## BlockProcessor

Each instruction block is parsed by using the Block Processor selected using
the mode key in the settings block. The job of a Block Processor is to transform
a JSON instruction block into a stage in memory. Block Processors are selected
by setting the mode key in the settings block. For example the kubectlblock
BlockProcessor is set by using the mode kubectl.

```json
...
"settings": {
	"mode":"kubectl",
    "varpath":"./data/"
}
...
```

The dolphin beta-2 project comes with the kubectlblock pre-loaded into the
modules but you can easily develop your own by following some simple conventions.

## The kubectlblock processor

This processor comes with a good number of useful commands to use.

**Main Instruction types**

- create
Creates kubernetes resource from YAML files or by making a [GET]
request to a repository for the YAML data.
- delete
Deletes a kubernetes resource from YAML files or by making a [GET]
request. to a repository for the YAML data.
- shell
Executes a basic shell command.

**Vars instruction types**

- ClusterIP
Select a service to store it's ClusterIP.
- STDOUT
Stores last instructions stdout.

**wait_for instruction types**

- PodStatus
Will not execute main instruction until selected pod's status is
in specified state.

## Creating the most basic dolphin deployment

Creating your first dolphin deployment is simple. Clone the repo and that's
all there is to it-you're ready to go!

```bash
python3 app/dolphin.py deploy \
-G https://raw.githubusercontent.com/andrewcampagnagit/dolphin/master/resources/instructions.json \
preload https://raw.githubusercontent.com/andrewcampagnagit/dolphin/beta-2/data/vars.json
```

Should output
```
Dolphin version beta-2.0
Created by Server Center - Cloud Development Software
```

Such a simple deployment yet a lot is happening behind the scenes to provide
this simple message.

Downloads instruction file remotely
```bash
--GET || -G
```

Downloads Vars remotely into vars.json in the specified vars path
```
preload
```

Go ahead and check out the content of these pages to get an idea of what is
going on.

You can deploy locally by using the options with a file path to the instructions
```bash
--file || -f
```


