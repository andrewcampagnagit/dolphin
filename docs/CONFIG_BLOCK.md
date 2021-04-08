# ConfigBlockProcessor (v1.0) Reference

## Instruction type selector 

Processor selector: **config**
Usage: **config<command>.<filetype>**

## Requirements

The user running the deploy application must have permission to read/write to the 
specified configuration files.

## Main Commands

[print, write]

#### print.json

Provided a valid JSONPath and JSON file you will be returned the value stored at
the specified key.

```json
{
	"type":"config.read.json",
	"filepath":"./example/config.json",
	"jsonpath":"$.app.meta.value",
}
```

#### write.json

Provided a valid JSONPath and JSON file you will alter the value at the specified key.

```json
{
	"type":"config.write.json",
	"filepath":"./example/config.json",
	"jsonpath":"$.app.meta.value",
	"value":"my value"
}
```