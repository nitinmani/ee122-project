from datetime import datetime
from random import *
#import numpy as np
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
		#print "For host: " + host.name + " the number of packets is: " + str(num)
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
				self.host_map[elem].throughput = self.host_map[elem].num_pkts/last_pkt_end*1.0

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
			host.throughput = host.num_pkts/last_pkt_end*1.0

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
				self.host_map[lst[idx]].throughput = self.host_map[lst[idx]].num_pkts/last_pkt_end*1.0
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
				self.host_map[lst[idx]].throughput = self.host_map[lst[idx]].num_pkts/last_pkt_end*1.0
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
		tickets = [i for i in range(100)]
		shuffle(tickets)
		last_pkt_end = 0
		tickets_A = tickets[:probs[0]]
		tickets_B = tickets[probs[0] : probs[0] + probs[1]]
		tickets_C = tickets[probs[0] + probs[1] : probs[0] + probs[1] + probs[2]]
		tickets_D = tickets[probs[0] + probs[1] + probs[2]:]
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
			if idx != 0: 
				queue = self.map[idx]
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				self.host_map[idx].add_pkt(item)
				if queue.empty():
					if idx == 1:
						tickets_A = None
						lst.remove(1)
					elif idx == 2:
						tickets_B = None
						lst.remove(2)
					elif idx == 3: 
						tickets_C = None
						lst.remove(3)
					else:
						tickets_D = None
						lst.remove(4)
					self.host_map[idx].TAT = last_pkt_end
					print(len(self.host_map[idx].processed_pkts))
					self.host_map[idx].throughput = len(self.host_map[idx].processed_pkts)/last_pkt_end*1.0

'''
	These will print out comma seperated values that you could copy as
	an array into the ipython notebook
'''

A = Host('A')
B = Host('B')
C = Host('C')
D = Host('D')
source = Source(A, B, C, D)




# #to print out the indices
# i = 1
# toPrint = ""
# while i < 100000:
# 	toPrint += str(i)
# 	toPrint +=  ","
# 	i += 1000
# print(toPrint)

# #This is for finding the individual throughputs
# #Throughput for varying the packets of the first source
# i = 1
# toPrint1 = ""
# toPrint2 = ""
# toPrint3 = ""
# toPrint4 = ""
# while i < 100000:
# 	source.populate_queue(source.A, A, i)
# 	source.populate_queue(source.B, B, 10000)
# 	source.populate_queue(source.C, C, 10000)
# 	source.populate_queue(source.D, D, 10000)
# 	#change this line to use other protocols
# 	source.rand()
# 	toPrint1 += str(A.throughput)
# 	toPrint1 += ","
# 	toPrint2 += str(B.throughput)
# 	toPrint2 += ","
# 	toPrint3 += str(C.throughput)
# 	toPrint3 += ","
# 	toPrint4 += str(D.throughput)
# 	toPrint4 += ","
# 	i += 1000
# print(toPrint1)
# print(toPrint2)
# print(toPrint3)
# print(toPrint4)

# #This is for finding the individual turnaroud times
# #TAT for varying the packets of the first source
# i = 10001
# toPrint1 = ""
# toPrint2 = ""
# toPrint3 = ""
# toPrint4 = ""
# while i < 100000:
# 	source.populate_queue(source.A, A, i)
# 	source.populate_queue(source.B, B, 10000)
# 	source.populate_queue(source.C, C, 10000)
# 	source.populate_queue(source.D, D, 10000)
# 	#change this line to use other protocols
# 	source.rand()
# 	toPrint1 += str(A.TAT)
# 	toPrint1 += ","
# 	toPrint2 += str(B.TAT)
# 	toPrint2 += ","
# 	toPrint3 += str(C.TAT)
# 	toPrint3 += ","
# 	toPrint4 += str(D.TAT)
# 	toPrint4 += ","
# 	i += 1000
# print(toPrint1)
# print(toPrint2)
# print(toPrint3)
# print(toPrint4)


#to print out the indices
i = 1
toPrint = ""
while i < 100000:
	toPrint += str(i)
	toPrint +=  ","
	i += 1000
print(toPrint)

#This is for finding the average throughputs
#Throughput for varying the packets of the first source
i = 1
toPrint1 = ""
while i < 100000:
	source.populate_queue(source.A, A, i)
	source.populate_queue(source.B, B, 10000)
	source.populate_queue(source.C, C, 10000)
	source.populate_queue(source.D, D, 10000)
	#change this line to use other protocols
	source.fifo()
	toPrint1 += str((A.throughput + B.throughput + C.throughput + D.throughput) / 4.0)
	toPrint1 += ","
	i += 1000
print(toPrint1)

#This is for finding the average turnaroud times
#TAT for varying the packets of the first source
i = 1
toPrint1 = ""
while i < 100000:
	source.populate_queue(source.A, A, i)
	source.populate_queue(source.B, B, 10000)
	source.populate_queue(source.C, C, 10000)
	source.populate_queue(source.D, D, 10000)
	#change this line to use other protocols
	source.fifo()
	toPrint1 += str((A.TAT + B.TAT + C.TAT + D.TAT) / 4.0)
	toPrint1 += ","
	i += 1000
print(toPrint1)

