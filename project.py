from datetime import datetime
from random import *
import numpy as np
import Queue

PACKET_SIZE = 10000 #bits
BANDWIDTH = 10000000 #bits/sec
TRANSMISSION_DELAY = 0.001



class Host:
	def __init__(self, name):
		self.name = name
		self.TAT = None
		self.num_pkts = None
		self.throughput = None
		self.processed_pkts = []

	def add_pkt(self, item):
		self.processed_pkts.append(item)

	def set_num_pkts(self, num):
		self.num_pkts = num

	def __str__(self):
		return "The host is: " + str(self.name) + ". The turnaround time is: " + str(self.TAT) + ". The throughput is: " + str(self.throughput)

class Packet:
	def __init__(self, host):
		self.host = host
		self.size = PACKET_SIZE
		self.start = None
		self.end = None

class Source:
	def __init__(self, host1, host2, host3, host4):
		self.A = Queue.Queue()
		self.B = Queue.Queue()
		self.C = Queue.Queue()
		self.D = Queue.Queue()
		self.map = {1: self.A, 2: self.B, 3: self.C, 4: self.D}
		self.host_map = {1: host1, 2: host2, 3: host3, 4: host4}

	def populate_queue(self, q, host, num=None):
		if num == None:
			num = randint(1000, 10000) #populate with between 1000 - 10000 packets
		print "For host: " + host.name + " the number of packets is: " + str(num)
		host.set_num_pkts(num)
		for i in range(num):
			q.put(Packet(host.name))

	def rand(self):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		while len(lst) > 0:
			elem = choice(lst)
			queue = self.map[elem]
			item = queue.get()
			item.start = last_pkt_end
			item.end = item.start + TRANSMISSION_DELAY
			last_pkt_end = item.end
			self.host_map[elem].add_pkt(item)
			if queue.empty():
				lst.remove(elem)
				self.host_map[elem].TAT = last_pkt_end
				self.host_map[elem].throughput = self.host_map[elem].num_pkts/1.0*last_pkt_end

	def fifo(self):
		# by default, assume A, B, C, D
		lst  = [1,2,3,4]
		last_pkt_end = 0
		for i in range(len(lst)):
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = host.num_pkts/last_pkt_end*1.0

	def sjf(self):
		# by default, assume A < B < C < D
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		for i in range(len(lst)):
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = host.num_pkts/1.0*last_pkt_end

	def rr(self):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		count = 0
		while len(lst) > 0:
			idx = count % len(lst)
			queue = self.map[lst[idx]]
			if not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				self.host_map[lst[idx]].add_pkt(item)
			if queue.empty():
				self.host_map[lst[idx]].TAT = last_pkt_end
				self.host_map[lst[idx]].throughput = self.host_map[lst[idx]].num_pkts/1.0*last_pkt_end
				lst.remove(lst[idx])
			count += 1

	def wrr(self, weights):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		count = 0
		while len(lst) > 0:
			idx = count % len(lst)
			queue = self.map[lst[idx]]
			if not queue.empty():
				weight = weights[lst[idx]]
				i = 0
				while i < weight and not queue.empty():
					item = queue.get()
					item.start = last_pkt_end
					item.end = item.start + TRANSMISSION_DELAY
					last_pkt_end = item.end
					self.host_map[lst[idx]].add_pkt(item)
					i += 1
			if queue.empty():
				self.host_map[lst[idx]].TAT = last_pkt_end
				self.host_map[lst[idx]].throughput = self.host_map[lst[idx]].num_pkts/1.0*last_pkt_end
				lst.remove(lst[idx])
			count += 1

	def fq(self):
		lst  = [1,2,3,4]
		for i in range(len(lst)):
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			last_pkt_end = 0
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY*4
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = host.num_pkts/last_pkt_end*1.0

	def wfq(self, weights):
		lst  = [1,2,3,4]
		total_weight = sum(weights)
		for i in range(len(lst)):
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			weight = weights[i+1]
			last_pkt_end = 0
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY*weight*1.0/total_weight
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = host.num_pkts/last_pkt_end*1.0

	def lottery(self, probs):
		#sum(probs) = 100
		lst = [1,2,3,4]
		tickets = np.arange(100)
		shuffle(tickets)
		last_pkt_end = 0
		tickets_A = tickets[:probs[0]]
		tickets_B = tickets[probs[0] : probs[1]]
		tickets_C = tickets[probs[1] : probs[2]]
		tickets_D = tickets[probs[2]:]
		while len(lst) > 0:
			tick = randint(0, 99)
			queue = None
			idx = 0
			if tickets_A != None and tick in tickets_A:
				idx = 1
			if tickets_B != None and tick in tickets_B:
				idx = 2
			if tickets_C != None and tick in tickets_C:
				idx = 3
			if tickets_D != None and tick in tickets_D:
				idx = 4
			queue = self.map[idx]
			item = queue.get()
			item.start = last_pkt_end
			item.end = item.start + TRANSMISSION_DELAY
			last_pkt_end = item.end
			self.host_map[idx].add_pkt(item)
			if queue.empty():
				if idx == 1:
					tickets_A = None
				elif idx == 2:
					tickets_B = None
				elif idx == 3: 
					tickets_C = None
				else:
					tickets_D = None
				self.host_map[idx].TAT = last_pkt_end
				self.host_map[idx].throughput = last_pkt_end*1.0/len(self.host_map[idx].processed_pkts)

## DO NOT MODIFY THESE LINES 
A = Host('A')
B = Host('B')
C = Host('C')
D = Host('D')
source = Source(A, B, C, D)
##


# Step 1: Before running each scheduling alg, populate the host queues. 
# populate_queue(queue, host, num_pkts)
# if num_pkts is None, then a random number of packets are generated
source.populate_queue(source.A, A, 10000)
source.populate_queue(source.B, B, 10000)
source.populate_queue(source.C, C, 10000)
source.populate_queue(source.D, D, 10000)

# Step 2: Run the algorithm (fifo, sjf, rand, rr, wrr, fq, wfq, lottery)
# if running fifo or sjf, the order the hosts are processed in is A, B, C, D
# if running sjf, make sure num_pkts(A) <= num_pkts(B) <= num_pkts(C) <= num_pkts(D)
print "\n\n"
print "Random Queueing"
source.rand()

# Step 3: Print the hosts to get information on the turnaround time and the packet throughput
print(A)
print(B)
print(C)
print(D)
print "\n\n"

# Step 4: Rinse and repeat
source.populate_queue(source.A, A, 10000)
source.populate_queue(source.B, B, 10000)
source.populate_queue(source.C, C, 10000)
source.populate_queue(source.D, D, 10000)
print "\n\n"
print "FIFO Queueing"
source.fifo()
print(A)
print(B)
print(C)
print(D)
print "\n\n"
source.populate_queue(source.A, A, 10000)
source.populate_queue(source.B, B, 10000)
source.populate_queue(source.C, C, 10000)
source.populate_queue(source.D, D, 10000)
print "\n\n"
print "Round Robin Queueing"
source.rr()
print(A)
print(B)
print(C)
print(D)
print "\n\n"
source.populate_queue(source.A, A, 10000)
source.populate_queue(source.B, B, 10000)
source.populate_queue(source.C, C, 10000)
source.populate_queue(source.D, D, 10000)
print "\n\n"
print "Weighted Round Robin Queueing"
source.wrr({1:10, 2:20, 3:30, 4:40})
print(A)
print(B)
print(C)
print(D)
print "\n\n"
print "Fair Queueing"
source.populate_queue(source.A, A, 10000)
source.populate_queue(source.B, B, 10000)
source.populate_queue(source.C, C, 10000)
source.populate_queue(source.D, D, 10000)
print "\n\n"
source.fq()
print(A)
print(B)
print(C)
print(D)
