# FIXME: [garampat@mavt.ethz.ch; 2021-03-23] fix cflags
BINARIES = run-mincmaes1
KORALICXX=$(shell python3 -m korali.cxx --compiler)
KORALICFLAGS=`python3 -m korali.cxx --cflags`
KORALILIBS=`python3 -m korali.cxx --libs`

.SECONDARY:
.PHONY: all
all: $(BINARIES)

$(BINARIES) : % : %.o
	$(KORALICXX) -o $@ $^ $(KORALILIBS)

%.o: %.cpp
	$(KORALICXX) -c $(KORALICFLAGS) $<

.PHONY: clean
clean:
	$(RM) $(BINARIES) *.o *.ti *.optrpt *.txt 
