//data element, also linked to prev and next elements
struct data {
	int src;
	int dest;
	int value;
	struct data * prev;
	struct data * next; 
};