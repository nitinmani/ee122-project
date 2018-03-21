#include <pthread.h>
#include "queue.h"

struct router {
	int wait_time; 
	//for simplicity only 5 possible links and destinations
	int rout_table[25]; 
	struct router * outlinks[5];
	pthread_mutex_t queue_lock;
	struct queue * q; 	
};