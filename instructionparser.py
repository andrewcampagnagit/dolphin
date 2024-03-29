import dolphinpkg.BlockProcessors.kubectlblock as kubectlblock
import dolphinpkg.BlockProcessors.configblock as configblock
import os
import time
import json


class InstructionParser():
    """Parser object configured for current running
    dolphin job...
    """

    def __init__(self, varpath):

        self.wait_for  = None
        self.main_cmd  = None
        self.var_cmd   = None
        self.processor = None
        self.varpath   = varpath

        if not os.path.exists(varpath):
            os.popen("mkdir -p "+ os.getcwd() +"/" + varpath)

    def _verboseout(self, block):
        """Verbose output...
        """

        print(block)

    def _setprocessor(self, block):
        """Sets the processor mode...
        """

        mode = block["type"].split(".")

        if mode[0] == "kubectl":
            self.processor = lambda block, varpath: kubectlblock.processblock(block, varpath)

        elif mode[0] == "config":
            self.processor = lambda block, varpath: configblock.processblock(block, varpath)

    def parseblock(self, block):
        """Parses instructions from block into useable datastructures...
        """
        
        self._setprocessor(block)
        block = self._insertvars(block)
        self.main_cmd, self.var_cmd, self.wait_for = self.processor(block, self.varpath)
        self._runblock()

    def run_test(self, test):
        """Runs test block and returns boolean value for the result of the
        specified test...
        """

        print(test)

        return os.popen(test["script"]).read() == test["expected_result"]

    def _runblock(self):
        """Runs instruction block...
        """

        self._runwait(self.wait_for)
        self._runmain(self.main_cmd)
        self._runvars(self.var_cmd)

    def _insertvars(self, block):
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

    def _runwait(self, wait_for):
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

    def _runvars(self, var_cmd):
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

    def _runmain(self, main_cmd):
        """Runs main command in instruction block...
        """

        if main_cmd:
            stdout = os.popen(main_cmd + " &").read()
            os.popen("BACK_PID=$!; wait $BACK_PID")
            print(stdout, end="")

            with open(".dolphin_last_out.log", "w+") as dolphin_log_file:
                dolphin_log_file.write(stdout)

        return