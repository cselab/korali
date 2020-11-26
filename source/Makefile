include Makefile.conf
# ==============================================================================
WARNINGFLAGS += -Wall -Wno-deprecated-declarations -Wno-cast-function-type -Wno-parentheses -Wfatal-errors

# ==============================================================================
CXXFLAGS  = -g $(OPTFLAGS)  $(CXXARCH) $(WARNINGFLAGS)
CXXFLAGS += -I. -I./external  
CXXFLAGS += $(MPIFLAGS)
CXXFLAGS += $(EIGENCFLAGS) 
CXXFLAGS += $(GSLCFLAGS)
CXXFLAGS += $(RTNORMCFLAGS)
CXXFLAGS += $(NNCFLAGS)
CXXFLAGS += $(LIBGPCFLAGS)
CXXFLAGS += $(LIBCOCFLAGS)
CXXFLAGS += $(PYBIND11INCLUDES)
CXXFLAGS += $(OMPFLAGS)
CXXFLAGS += $(PTHREADFLAGS)

LDFLAGS = $(SHAREDLIB_FLAG)
LDFLAGS += $(RTNORMLIBS)
LDFLAGS += $(BLASLIBS)
LDFLAGS += $(GSLLIBS) 
LDFLAGS += $(NNLIBS)
LDFLAGS += $(LIBGPLIBS)
LDFLAGS += $(LIBCOLIBS)
LDFLAGS += $(PYTHONLIBS)
LDFLAGS += $(OMPFLAGS)
LDFLAGS += $(PTHREADFLAGS)

DEPFLAGS = -MT $@ -MD -MP -MF $(DEPDIR)/$*.Td

COMPILE.cc = $(CXX) $(DEPFLAGS) $(CXXFLAGS) -fPIC -c -o $@
LINK.o = $(CXX) -o $@
PRECOMPILE =
POSTCOMPILE = @mv -f $(DEPDIR)/$*.Td $(DEPDIR)/$*.d

# ==============================================================================
SOURCES = $(shell find . -name "*.cpp")
BUILDFILES = $(shell find . -name "build.py")

OBJDIR := .o
DEPDIR := .d

OBJS := $(patsubst %,$(OBJDIR)/%.o,$(basename $(SOURCES)))
DEPS := $(patsubst %,$(DEPDIR)/%.d,$(basename $(SOURCES)))

$(shell mkdir -p $(dir $(OBJS)) >/dev/null)
$(shell mkdir -p $(dir $(DEPS)) >/dev/null)
# ==============================================================================

.PHONY: clean all

all: libkorali.so

clean:
	@rm -f `find . -name "*._hpp" | sed 's/._hpp/.hpp/g'`
	@rm -f `find . -name "*._cpp" | sed 's/._cpp/.cpp/g'`
	@rm -f `find . -name "*.o" -not -type d` 
	@rm -f  *.so *.a $(OBJECTS)
	@rm -rf $(OBJDIR) $(DEPDIR)

build:
	@for buildfile in $(BUILDFILES); do python3 $$buildfile; done

libkorali.so: $(OBJS)
	$(LINK.o) $^ $(LDFLAGS) $(LDLIBS)

$(OBJDIR)/%.o: %.cpp
$(OBJDIR)/%.o: %.cpp $(DEPDIR)/%.d
	$(PRECOMPILE)
	$(COMPILE.cc) $<
	$(POSTCOMPILE)

.PRECIOUS = $(DEPDIR)/%.d
$(DEPDIR)/%.d: ;

-include $(DEPS)
