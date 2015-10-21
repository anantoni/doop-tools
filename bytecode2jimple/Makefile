buildDir    := build
srcDir      := name/bravenboer/martin/soot
sootClasses := ../../lib/sootclasses-2.5.0.jar
sootLibDir  := $(shell readlink -f $(sootClasses))
classes     := BytecodeToJimple BytecodeToJimple$$Mode NoSearchingClassProvider NoSearchingClassProvider$$FileResource NoSearchingClassProvider$$Resource NoSearchingClassProvider$$ZipEntryResource
classes     := $(classes:%=$(buildDir)/$(srcDir)/%.class)
jar         := soot-tools.jar
b2j         := ../bin/bytecode2jimple

.PHONY: all clean

all: $(buildDir) $(b2j)

$(buildDir):
	mkdir -p $@

$(classes): $(srcDir)/BytecodeToJimple.java $(srcDir)/NoSearchingClassProvider.java
	javac -Xlint -cp $(sootLibDir) -d $(buildDir) $^

$(jar): $(classes)
	jar cf $@ -C $(buildDir) .

$(b2j): $(jar)
	echo "#!/bin/bash" > $@
	echo "cp=$(sootLibDir):$(shell readlink -f $<)" >> $@
	echo 'java -cp $$cp name.bravenboer.martin.soot.BytecodeToJimple $$*' >> $@
	chmod +x $@


clean:
	rm -rf $(buildDir) $(jar) $(b2j)
