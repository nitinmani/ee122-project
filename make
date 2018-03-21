all: project

project: queue.o data.o router.o source.o destination.o
    g++ main.o factorial.o hello.o -o project

queue.o: main.c
    g++ -c main.c

data.o: factorial.c
    g++ -c factorial.c

source.o: hello.c
    g++ -c hello.c

