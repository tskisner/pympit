

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <time.h>


int main ( int argc, char *argv[] ) {

    int ret;
    int threadprovided;
    double * data;
    double * red;
    int n = 100000;
    int i;

    int rank;
    int np;

    time_t thetime;
    struct tm * timeinfo;

    time ( &thetime );
    timeinfo = localtime ( &thetime );

    ret = MPI_Init_thread ( &argc, &argv, MPI_THREAD_FUNNELED, &threadprovided );

    ret = MPI_Comm_size ( MPI_COMM_WORLD, &np );
    ret = MPI_Comm_rank ( MPI_COMM_WORLD, &rank );

    if ( rank == 0 ) {
        printf ( "Start main: %s", asctime (timeinfo) );
    }

    time ( &thetime );
    timeinfo = localtime ( &thetime );

    if ( rank == 0 ) {
        printf ( "Finish MPI init: %s", asctime (timeinfo) );
    }

    data = (double*) calloc ( n, sizeof(double) );
    if ( rank == 0 ) {
        red = (double*) calloc ( n, sizeof(double) );
    }

    if ( ( data == NULL ) || ( red == NULL ) ) {
        fprintf ( stderr, "Cannot allocate memory\n" );
        ret = MPI_Finalize();
        return 1;
    }

    for ( i = 0; i < n; ++i ) {
        data[i] = (double)rank;
    }

    ret = MPI_Allreduce ( (void *) data, (void *) red, n, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD );

    free ( data );
    if ( rank == 0 ) {
        free ( red );
    }

    time ( &thetime );
    timeinfo = localtime ( &thetime );

    if ( rank == 0 ) {
        printf ( "Finalizing MPI: %s", asctime (timeinfo) );
    }

    ret = MPI_Finalize ( );

    return ret;
}

