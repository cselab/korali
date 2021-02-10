BINARIES = run-gfpt run-vracer run-ddpg
KORALICXX=$(shell python3 -m korali.cxx --compiler)
KORALICFLAGS=`python3 -m korali.cxx --cflags`
KORALILIBS=`python3 -m korali.cxx --libs`

MSODECFLAGS=-I_deps/msode/src -I../_deps/msode/src -I_deps/msode/extern/json/include/ -I. -DNDEBUG -O3
MSODELIBS=_deps/msode/build/lib/libgtest.a \
         _deps/msode/build/src/msode/rl/librl.a\
         -lpthread \
         _deps/msode/build/src/msode/analytic_control/libanalytic_control.a\
         _deps/msode/build/src/msode/utils/libutils.a \
         _deps/msode/build/src/msode/core/libmsode.a \
         -lbfd -ldl

.SECONDARY:
.PHONY: all 
all: $(BINARIES)

$(BINARIES) : % : %.o environment.o
	$(KORALICXX) -o $@ $^ $(KORALILIBS) $(MSODELIBS)

%.o: %.cpp
	$(KORALICXX) -c $< $(KORALICFLAGS) $(MSODECFLAGS)

environment.o: _environment/environment.cpp
	$(KORALICXX) -c $< $(KORALICFLAGS) $(MSODECFLAGS)

.PHONY: clean
clean:
		$(RM) $(BINARIES) *.o *.ti *.optrpt *.h5 *.dat *.xmf
