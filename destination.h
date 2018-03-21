#include <pthread.h>
#include "data.h"

struct destination {
	pthread_mutex_t queue_lock;
	struct data * queue;
};