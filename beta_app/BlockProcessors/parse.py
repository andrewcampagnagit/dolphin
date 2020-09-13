import BlockProcessors.kubectlblock as kubectlblock
import os
import time
import json


class InstructionParser():
    """Parser object configured for current running
    dolphin job...
    """

    def __init__(self, mode, varpath):

        self.wait_for = None
        self.main_cmd = None
        self.var_cmd = None
        self.processor = None
        self.varpath = varpath

        if mode == "kubectl":
            self.processor = lambda block: kubectlblock.processblock(block)

    def parseblock(self, block):
        """Parses instructions from block into useable datastructures...
        """

        block = self.insertvars(block)
        self.main_cmd, self.var_cmd, self.wait_for = self.processor(block)
        self.runblock()

    def runblock(self):
        """Runs instruction block...
        """

        self.runwait(self.wait_for)
        self.runmain(self.main_cmd)
        self.runvars(self.var_cmd)

    def insertvars(self, block):
        """Replaces var keys with values inside instruction block...
        """

        with open(self.varpath + "vars.json", "r") as var_file:
            var_dict = json.load(var_file)

        block_str = json.dumps(block)

        while "%" in block_str:
            index_1 = block_str.find("%") + 1
            index_2 = block_str.find("%", index_1 + 1)
            variable = block_str[index_1:index_2]
            block_str = block_str.replace(
                "%" + variable + "%", var_dict[variable])
        return json.loads(block_str)

    def runwait(self, wait_for):
        """Runs wait command until specified condition is true...
        """

        if wait_for:
            for wait in wait_for:
                while(True):
                    print("waiting for..." + wait["selector"])
                    if os.popen(wait["cmd"]).read().split()[
                            0] == wait["value"].split()[0]:
                        break
                    time.sleep(wait["buffer"])
        return

    def runvars(self, var_cmd):
        """Stores vars into dictionary and writes to file in varpath...
        """

        var_dict = {}

        if os.path.exists(self.varpath + "/vars.json"):
            with open(self.varpath + "/vars.json", "r") as var_file:
                var_dict = json.load(var_file)

        if var_cmd:
            for var_block in var_cmd:
                var_dict[var_block[0]] = os.popen(
                    var_block[1]).read().replace("\n", "")

        with open(self.varpath + "/vars.json", "w+") as var_file:
            json.dump(var_dict, var_file)

        return

    def runmain(self, main_cmd):
        """Runs main command in instruction block...
        """

        if main_cmd:
            print(os.popen(main_cmd).read(), end="")
        return
