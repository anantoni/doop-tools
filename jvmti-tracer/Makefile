CC      := gcc
JAVAC   := javac
LDFLAGS := -fPIC -I$(JAVA_HOME)/include -I$(JAVA_HOME)/include/linux 

SRCDIR  := ./src
DESTDIR := ./build
TARGETS := $(addprefix $(DESTDIR)/, Trace2GXL.class tracer.so)

PROBE = ../probe/probe.jar

all: $(TARGETS)

vpath %.c    $(SRCDIR)
vpath %.java $(SRCDIR)

$(DESTDIR)/%.so: %.c | $(DESTDIR)
	$(CC) $(LDFLAGS) -O2 -shared -o $@ $<

$(DESTDIR)/%.class: %.java | $(DESTDIR)
	$(JAVAC) -cp $(PROBE) -d $(DESTDIR)/ $<

clean:
	rm -rf $(DESTDIR)/

$(DESTDIR):
	mkdir -p $@

.PHONY: all clean
