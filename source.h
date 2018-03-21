#include <pthread.h>
#include "router.h"

struct source {
	int wait_time; 
	//for simplicity only 5 possible links and destinations
	int rout_table[25];
	struct router * outlinks[5];
	struct queue * q; 
};

