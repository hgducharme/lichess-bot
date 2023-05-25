appname := meatball

CXX := clang++
CPPFLAGS := -g -fdiagnostics-color=always -std=c++17'
# LDFLAGS := 
# LDLIBS := 
remove := rm -f

sourcefiles := $(shell find . -name "*.cpp")
objectfiles := $(patsubst %.cpp, %.o, $(sourcefiles))

all: $(appname)

$(appname): $(objectfiles)
	$(CXX) $(CPPFLAGS) $(LDFLAGS) -o $(appname) $(objectfiles) $(LDLIBS)

depend: .depend

.depend: $(sourcefilemakes)
	$(remove) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(remove) $(objectfiles)

distclean:
	$(remove) *~ .depend

include .depend