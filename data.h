//data element, also linked to prev and next elements
#include <time.h>

struct data {
	int src;
	int dest;
	int value;
	struct data * prev;
	struct data * next; 
	size_t data_size;
	clock_t enqueue_time;
	clock_t dequeue_time;
	clock_t queue_delay;
};

double transmission_delay(struct data * pkt, double bandwidth) {
	return (double) pkt->data_size*1.0/bandwidth;
};

void enqueue(struct data * pkt) {
	pkt->enqueue_time = clock();
};

void dequeue(struct data * pkt) {
	pkt->dequeue_time = clock();
	pkt->queue_delay = (double)(pkt->dequeue_time - pkt->enqueue_time) / CLOCKS_PER_SEC;
};
