SHELL = /bin/bash

CC = mpicc
CFLAGS = -O3 -fPIC


all : pympit_compiled


pympit_compiled : pympit_compiled.o
	$(CC) -o pympit_compiled pympit_compiled.o

pympit_compiled.o : pympit_compiled.c
	$(CC) $(CFLAGS) -o pympit_compiled.o -c pympit_compiled.c


clean :
	@rm -f pympit_compiled *.o *~

