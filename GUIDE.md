# How to use dolphin (beta-2)

### Getting started

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

### Blocks and stages

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
to as **stages** which are the raw shell commands that actually do the resource
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




