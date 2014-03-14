CC = gcc
JC = javac
LD_FLAGS = -fPIC -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux 

SRCDIR  = ./src/
DESTDIR = ./build/
TARGETS = $(addprefix $(DESTDIR), Trace2GXL.class tracer.so)

PROBE = ../probe/probe.jar

all: $(TARGETS)

$(DESTDIR)%.so: $(SRCDIR)%.c	
	$(CC) $(LD_FLAGS) -shared -o $@ $<

$(DESTDIR)%.class: $(SRCDIR)%.java
	$(JC) -cp $(PROBE) -d $(DESTDIR) $<

clean:
	rm -rf $(DESTDIR)

installdirs:
	mkdir -p $(DESTDIR)

$(TARGETS): installdirs

.PHONY: all clean installdirs
