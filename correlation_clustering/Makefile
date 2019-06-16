####################################################
###################### MAKE ########################
####################################################

EXECUTAVEL = CCP
PATHEXEC = ../data/cc
PATHSRC= ./src
PATHTEMP = ./.temp

all:
	mkdir -p $(PATHEXEC)
	mkdir -p $(PATHTEMP)
	make $(EXECUTAVEL)

#Group object files and building the program
$(EXECUTAVEL): $(PATHTEMP)/Solution.o $(PATHTEMP)/Exact.o $(PATHTEMP)/Edge.o $(PATHTEMP)/EdgeList.o $(PATHTEMP)/Instance.o $(PATHTEMP)/main.o
	$(CPP) $(CCFLAGS) $(PATHTEMP)/Solution.o $(PATHTEMP)/Exact.o $(PATHTEMP)/Edge.o $(PATHTEMP)/EdgeList.o $(PATHTEMP)/Instance.o $(PATHTEMP)/main.o $(CCLNFLAGS) -o $(PATHEXEC)/$(EXECUTAVEL) -lrt

$(PATHTEMP)/main.o: $(PATHSRC)/main.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/main.cpp -o $(PATHTEMP)/main.o

$(PATHTEMP)/Instance.o: $(PATHSRC)/instance.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/instance.cpp -o $(PATHTEMP)/Instance.o

$(PATHTEMP)/EdgeList.o: $(PATHSRC)/edge_list.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/edge_list.cpp -o $(PATHTEMP)/EdgeList.o

$(PATHTEMP)/Edge.o: $(PATHSRC)/edge.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/edge.cpp -o $(PATHTEMP)/Edge.o

$(PATHTEMP)/Exact.o: $(PATHSRC)/exato.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/exato.cpp -o $(PATHTEMP)/Exact.o
	
$(PATHTEMP)/Solution.o: $(PATHSRC)/Solution.cpp
	$(CPP) $(CCFLAGS) -c $(PATHSRC)/Solution.cpp -o $(PATHTEMP)/Solution.o

####################################################
###################### CLEAN #######################
####################################################
clean:
	rm -rf $(PATHEXEC)
	rm -rf $(PATHTEMP)

####################################################
####################### CPLEX ######################
####################################################

##### CPLEX CONFIGURATION's
# System architecture
SYSTEM = x86-64_linux
# Static library format for Cplex
LIBFORMAT = static_pic
# Cplex directory
CPLEXDIR = /opt/ibm/ILOG/CPLEX_Studio128/cplex
# Concert directory
CONCERTDIR = /opt/ibm/ILOG/CPLEX_Studio128/concert

##### CPLEX DIRECTIVE's
# Cplex static libraries directory
CPLEXLIBDIR = $(CPLEXDIR)/lib/$(SYSTEM)/$(LIBFORMAT)
# Concert static libraries directory
CONCERTLIBDIR = $(CONCERTDIR)/lib/$(SYSTEM)/$(LIBFORMAT)
# Cplex header's directory
CPLEXINCDIR = $(CPLEXDIR)/include
# Concert header's directory
CONCERTINCDIR = $(CONCERTDIR)/include

####################################################
################### LOCAL SOLVER ###################
####################################################

LSOLVERDIR 	  = /opt/localsolver_7_5
LSOLVERINDIR = $(LSOLVERDIR)/include

####################################################
##################### COMPILER #####################
####################################################

##### COMPILER CONFIGURATION's
# Compiler
CPP = g++ -std=c++11
# Compilation parameters
CCOPT = -Ofast -g -fPIC -fexceptions -DIL_STD #-DDEBUG
## Include libraries identifiers
CCLNFLAGS = -L$(CPLEXLIBDIR) -lilocplex -lcplex -L$(CONCERTLIBDIR) -lconcert -m64 -lm -pthread -ldl
# Header's include path
CCFLAGS = $(CCOPT) -I$(CPLEXINCDIR) -I$(CONCERTINCDIR) -I$(LSOLVERINDIR)