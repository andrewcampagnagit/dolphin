# dolphin 

[![Generic badge](https://img.shields.io/badge/python-3.7-blue)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/dolphin-beta--3-orange)](https://shields.io)

#### Summary

Dolphin aims to ease the multistage cloud application deployment process by creating instruction blocks for each part of the process. What makes this process different is the robust set of functionality that dolphin features in its templates. You can specify instruction blocks to store variables from deployed resources dynamically. Another great feature is the ability to impose a wait instruction on a resource; this halts all operations from that point in the deployment until a specific condition is met, like a pod in Running status. These features come with our of the box BlockProcessors, but you can write your custom processor quickly.

#### Fast start guide

Dolphin is packaged into a Red Hat Enterprise Linux container image for the best cross platform compatability.

**For Linux users** We reccomend podman
**For Windows, Mac, and all other OS** We reccomend docker

Pull down the image from quay.io
```bash
podman pull quay.io/dolphin/dolphin:latest
```
or 
```bash
docker pull quay.io/dolphin/dolphin:latest
```

Run the example instructions
```bash
podman run dolphin:latest deploy -mF /dolphin/example/manifest.json
```
or
```bash
docker run dolphin:latest deploy -mF /dolphin/example/manifest.json
```

You should see the output of the example deployment to confirm your dolphin deployment container is functioning properly
```bash
*******************************************************
Dolphin - Cloud deployment and packaging framework.
dolphindev.com				   (beta-3)
*******************************************************
['dolphin.py', 'deploy', '-mF', '/dolphin/example/manifest.json']

Gathering resources...
*******************************************************
Loading manifest from file /dolphin/example/manifest.json
[GET]**************************************************
Downloading instructions from https://raw.githubusercontent.com/andrewcampagnagit/dolphin/beta-3/example/instructions.json
Placing instructions into ./tmp/instructions.json
[GET]**************************************************
Downloading vars from https://raw.githubusercontent.com/andrewcampagnagit/dolphin/beta-3/example/vars.json
Placing vars into ./tmp/vars.json
[INSTRUCTION BLOCK]************************************
Hello dolphin!
Version: beta-3
[TEST BLOCK]*******************************************
{'script': 'echo "test"', 'expected_result': 'test\n'}
PASS
[TEST BLOCK]*******************************************
{'script': 'echo "test1"', 'expected_result': 'test1\n'}
PASS
[TEST BLOCK]*******************************************
{'script': 'echo "test2"', 'expected_result': 'test2\n'}
PASS
[CLEAN UP]*********************************************
Cleaning up...
```

You're ready to go! See below for more information.

**Comprehensive guide** <URL_TO_GUIDE>

**Project contribution rules** <URL_TO_HOW_TO_CONTRIBUTE>


