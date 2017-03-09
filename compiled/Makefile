SHELL = /bin/bash

ifndef CC
  CC = mpicc
endif

ifndef CFLAGS
  CFLAGS = -O3 -fPIC
endif


all : pympit_compiled


pympit_compiled : pympit_compiled.o
	$(CC) -shared -o pympit_compiled pympit_compiled.o

pympit_compiled.o : pympit_compiled.c
	$(CC) $(CFLAGS) -o pympit_compiled.o -c pympit_compiled.c


clean :
	@rm -f pympit_compiled *.o *~

