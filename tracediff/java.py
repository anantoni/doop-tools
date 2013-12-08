import os, zipfile

class Env:

    JAVA_HOME = os.environ['JAVA_HOME']

    def __init__(self, classpath):
        self._jars = [os.path.expanduser(x) for x in classpath.split(':')]
        self._classes = set()

        jarpath = os.path.join(self.JAVA_HOME, 'jre', 'lib')

        for jar in os.listdir(jarpath):
            if jar.endswith(".jar"):
                self._jars.append(os.path.join(jarpath, jar))

        for i in self._jars:
            # print i
            for c in self.classlist(i):
                self._classes.add(c)

    def __contains__(self, klass):
        return klass in self._classes

    @classmethod
    def classlist(cls, jarpath):
        jar = zipfile.ZipFile(jarpath, 'r')
        try:
            for entry in jar.namelist():
                if not entry.endswith('.class'):
                    continue
                yield entry[:-len('.class')].replace('/','.')
        finally:
            jar.close()
