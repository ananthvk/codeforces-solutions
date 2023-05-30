CXX=clang++
CXXFLAGS=-O3
INCLUDE_FLAGS=-I../include

build: nanobench.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDE_FLAGS) nanobench.cpp -c -o nanobench.o
	ar -rvs libnanobench.a nanobench.o
	rm nanobench.o
	mkdir -p ../lib
	mv libnanobench.a ../lib

clean:
	rm -rf *.o
	rm -rf *.a