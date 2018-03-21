#include "data.h" 
#include <stdlib.h>
#include <stdio.h>

//linked lists are bare recursive and start with a sentinal

struct queue {
	struct data * first;
	struct data * last; 
};

void init_queue(struct queue * q) {
	q->first = malloc(sizeof(struct data));
	q->last = malloc(sizeof(struct data));
	q->first->prev = 0;
	q->first->next = q->last;
	q->last->prev = q->first; 
	q->last->next = 0; 
};

struct data * dequeue (struct queue * q) {
	struct data * toReturn = 0;
	if (q->first->next != q->last) {
		toReturn = q->first->next; 
		q->first->next = q->first->next->next;
		q->first->next->prev = q->first; 
		toReturn -> prev = 0;
		toReturn -> next = 0; 
	}
	return toReturn; 
};

void enqueue (struct queue * q, struct data * next) { 
	next -> prev = q->last->prev;
	next->next = q->last;
	q->last->prev->next = next;
	q->last->prev = next;
};

void free_queue(struct queue * q) {
	free(q->first);
	free(q->last); 
}