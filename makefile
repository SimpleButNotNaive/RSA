CC := g++
FLAGS := --std=c++14 -g
CPP := $(wildcard *.cpp)
HPP := $(wildcard *.hpp)

main:$(CPP) $(HPP)
	@$(CC) $(CPP) $(FLAGS) -o $@