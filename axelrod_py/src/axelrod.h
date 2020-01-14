#include <stdio.h>
#include <stdlib.h>

#ifndef AXL_NETWORK
#define AXL_NETWORK

/*
Axelrod network with n agents
*/
struct _axl_network
{
	int nagents; /* Number of axelrod agents in the network */
	int **a;
	int **corr;
};
typedef struct _axl_network axl_network;
#endif


#ifndef ACTIVE_LINK
#define ACTIVE_LINK

struct _active_link{
        int source;
        int target;
};
typedef struct _active_link active_link;

#endif
