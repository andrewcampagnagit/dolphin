# Dolphin Beta-3 Guide

In this guide, you will learn the how to create and deploy dolphin packages, work with vars, create test blocks, utilize various useful command-line options, and develop custom BlockProcessors.

## Architecture

## Create your first dolphin package and deploy

Getting started is quick and easy with the dolphin packager. Simply use the **create** option with the **package** command to generate a boilerplate for your project. 

```bash
dolphin package create <package_name>
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
