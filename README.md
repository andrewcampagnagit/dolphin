# dolphin 

[![Generic badge](https://img.shields.io/badge/python-3.7-blue)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/dolphin-beta--4-orange)](https://shields.io)

#### Summary

Dolphin aims to ease the multistage cloud application deployment process by creating instruction blocks for each part of the process. What makes this process different is the robust set of functionality that dolphin features in its templates. You can specify instruction blocks to store variables from deployed resources dynamically. Another great feature is the ability to impose a wait instruction on a resource; this halts all operations from that point in the deployment until a specific condition is met, like a pod in Running status. For additional functionality, you can develop custom BlockProcessors to add functionality.

#### Whats new?

- Mode switching: Easily use multiple BlockProcessors in your instructions file
- ConfigBlockProcessor: New out-of-box BlockProcessor for modifying various configuration files
- Colorama fixes: Multiple terminal colorama bugs have been fixed
- Logging: Advanced logging features & debugging features **(Still developing)**
- Health: Re-run test blocks alone or develop test block only instruction files for health checking **(Beta released!)**
- History: See deployment and test result history **(Beta released!)**
- Repository server: Run dolphin as a stand alone repository server **(Still developing)**

#### Fast start guide

Clone the repository
```bash
git clone https://github.com/andrewcampagnagit/dolphin.git
```

Run the setup shell script
```bash
bash setup.sh
```

Create a default package
```bash
dolphin package-create test
```

Run the instructions in the package
```bash
dolphin deploy -f test/instructions.json
```

You should see the output of the example deployment to confirm your dolphin deployment container is functioning properly
```bash
*******************************************************
Dolphin - Cloud deployment and packaging framework.
dolphindev.com				   (beta-4)
*******************************************************
['/usr/local/bin/dolphin', 'deploy', '-f', 'test/instructions.json']
Gathering resources...
{'instructions_file': 'test/instructions.json'}
[INSTRUCTION BLOCK]************************************
Hello dolphin!
Version: beta-4
[TEST BLOCK]*******************************************
{'script': 'echo "It works!"', 'expected_result': 'It works!\n'}
PASS
{'time': 'May 06 2021 @ 10:17:47:380248 AM', 'meta': {'name': 'test', 'generatedBy': 'dolphin packager'}, 'id': '6e7e80514d734888b5cd33b38efd9a7e', 'tests': {0: {'script': 'echo "It works!"', 'status': 'Pass'}}, 'status': 'DeploySuccessful'}
```

You're ready to go! See below for more information.

**Comprehensive guide** https://github.com/andrewcampagnagit/dolphin/blob/beta-4/docs/GUIDE.md

**Project contribution rules** https://github.com/andrewcampagnagit/dolphin/blob/beta-4/docs/CONTRIB_RULES.md


