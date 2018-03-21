#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include "source.h"



int table_width = 5;
int table_height = 5;  

void table_set(int * table, int i, int j, int value) {
	table[table_width * i + j] = value; 
} 

int table_get(int * table, int i, int j) {
	return table[table_width * i + j];
}

void * src_thread(struct source * contents) {
    struct data * curr; 
	while ((curr = dequeue(contents->q))) {
   		//find the next hop in the routing table and send it there
    	if (curr) {
    		for (int i = 0; i < 5; i++) {
    			for (int j = 0; j < 5; j++) {
    				if(contents->rout_table[5 * i + j] == curr->dest) {
    					pthread_mutex_lock(&(contents->outlinks[i]->queue_lock)); 
    					enqueue(contents->outlinks[i]->q, curr);
    					pthread_mutex_unlock(&(contents->outlinks[i]->queue_lock));
    			}
    		}
    	}
		//set the time between sending, in seconds  
	   }
       sleep(contents->wait_time);
    } 
}

void * router_thread(struct router *  contents) {
	while (1) {
		pthread_mutex_lock(&(contents->queue_lock));
    	struct data * curr = dequeue(contents->q);
   		//find the next hop in the routing table and send it there
    	if (curr) {
    		for (int i = 0; i < 5; i++) {
    			for (int j = 0; j < 5; j++) {
    				if(contents->rout_table[5 * i + j] == curr->dest) {
    					pthread_mutex_lock(&(contents->outlinks[i]->queue_lock)); 
    					enqueue(contents->outlinks[i]->q, curr);
    					pthread_mutex_unlock(&(contents->outlinks[i]->queue_lock));
                    }
    			}
    		}
    	}

		pthread_mutex_unlock(&(contents->queue_lock));
		//set the service time, in seconds
		sleep(contents->wait_time); 
	}
}

void * destination_thread(struct router * contents) {
	while (1) {
		pthread_mutex_lock(&(contents->queue_lock));
    	
    	struct data * curr = dequeue(contents->q);
    	while (curr) {
    		printf("success got %d \n", curr->value);
    		curr = dequeue(contents->q);
    		//data value has reached end can be freed
    		free(curr); 
    	}
		pthread_mutex_unlock(&(contents->queue_lock));
		sleep(contents->wait_time); 
	}
}

int main () {
    pthread_t th_s1;
    pthread_t th_r1;

    struct source s1;
    struct router r1;
    struct router r2;

    //initializing source
    struct queue q1;
    init_queue(&q1);
    struct data d1 = {1,2,666,0,0};
    struct data d2 = {1,2,777,0,0};
    struct data d3 = {1,2,888,0,0};
    enqueue(&q1, &d1);
    enqueue(&q1, &d2);
    enqueue(&q1, &d3);
    s1.wait_time = 1;
    s1.rout_table[0] = 2;
    s1.outlinks[0] = &r1; 
    s1.q = &q1;

    //initializing router 1
    struct queue q2;
    init_queue(&q2);
    r1.q = &q2;
    s1.rout_table[0] = 2;
    s1.outlinks[0] = &r2;
    pthread_mutex_init(&(r1.queue_lock), NULL); 

    //initializing router 2
    struct queue q3;
    init_queue(&q3);
    r2.q = &q3;
    pthread_mutex_init(&(r2.queue_lock), NULL); 
                        

    pthread_create(&th_r1, NULL, destination_thread, &r2);
    pthread_create(&th_r1, NULL, router_thread, &r1);
    pthread_create(&th_s1, NULL, src_thread, &s1);
    
    pthread_join(th_s1, NULL);

    free_queue(&q1);
    free_queue(&q2); 

    return 0; 
}