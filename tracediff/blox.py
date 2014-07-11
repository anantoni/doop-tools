import subprocess

class Connector:
    def __init__(self, workspace):
        self._workspace = workspace

    def query(self, queryString, **kwargs):
        results = []
        command = "bloxbatch.sh -db %s -query '%s' " % (self._workspace, queryString)

        # Optional argument
        if "toprint" in kwargs:
            command += "print %s" % (kwargs["toprint"],)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p.stdout.readlines():
            results.append(line.strip())

        p.wait()
        return results
