sootClasses = ../../lib/sootclasses-2.5.0.jar
exe         = ../bin/bytecode2jimple

all:
	$(eval tmpDir    := $(shell mktemp -d))
	$(eval javaFiles := $(shell find name -name '*.java'))
	$(eval currentDir:= $(shell pwd))
	$(eval sootLibDir:= $(shell readlink -f $(sootClasses)))

	mkdir $(tmpDir)/content
	javac -Xlint -cp $(sootLibDir) -d $(tmpDir)/content $(javaFiles)
	jar cvf $(tmpDir)/soot-tools.jar -C $(tmpDir)/content .
	cp $(tmpDir)/soot-tools.jar .
	rm -rf $(tmpDir)

	echo "#!/bin/bash" > $(exe)
	echo "cp=$(sootLibDir):$(currentDir)/soot-tools.jar" >> $(exe)
	echo 'java -cp $$cp name.bravenboer.martin.soot.BytecodeToJimple $$*' >> $(exe)
	chmod +x $(exe)
