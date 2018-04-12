from datetime import datetime
from random import *
import numpy as np
import Queue

PACKET_SIZE = 10000 #bits
BANDWIDTH = 1000000 #bits/sec
TRANSMISSION_DELAY = 0.01



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

class Packet:
	def __init__(self, host):
		self.host = host
		self.size = PACKET_SIZE
		self.start = None
		self.end = None

class Source:
	def __init__(self):
		self.A = Queue.Queue()
		self.B = Queue.Queue()
		self.C = Queue.Queue()
		self.D = Queue.Queue()
		self.map = {1: self.A, 2: self.B, 3: self.C, 4: self.D}
		self.host_map = {1: Host('A'), 2: Host('B'), 3: Host('C'), 4: Host('D')}

	def populate_queue(self, q, host, num=None):
		if num == None:
			num = randint(1000, 10000) #populate with between 1000 - 10000 packets
		host.set_num_pkts(num)
		for i in range(num):
			q.put(Packet(host.name))

	def random(self):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		while len(lst) > 0:
			elem = random.choice(lst)
			queue = self.map[elem]
			item = queue.get()
			item.start = last_pkt_end
			item.end = item.start + TRANSMISSION_DELAY
			last_pkt_end = item.end
			self.host_map[elem].add_pkt(item)
			if queue.empty():
				lst.remove(elem)
				self.host_map[elem].TAT = last_pkt_end
				self.host_map[elem].throughput = last_pkt_end*1.0/len(self.host_map[elem].processed_pkts)

	def fifo(self):
		# by default, assume A, B, C, D
		lst  = [1,2,3,4]
		last_pkt_end = 0
		for i in range(len(lst))
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = last_pkt_end*1.0/len(host.processed_pkts)

	def sjf(self):
		# by default, assume A < B < C < D
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		for i in range(len(lst))
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = last_pkt_end*1.0/len(host.processed_pkts)

	def rr(self):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		count = 0
		while len(lst) > 0:
			idx = count % 4
			queue = self.map[lst[idx]]
			if not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY
				last_pkt_end = item.end
				self.host_map[idx].add_pkt(item)
			if queue.empty():
				lst.remove(elem)
				self.host_map[idx].TAT = last_pkt_end
				self.host_map[idx].throughput = last_pkt_end*1.0/len(self.host_map[idx].processed_pkts)
			count += 1

	def wrr(self, weights):
		lst = [1, 2, 3, 4]
		last_pkt_end = 0
		count = 0
		while len(lst) > 0:
			idx = count % 4
			queue = self.map[lst[idx]]
			if not queue.empty():
				weight = weights[idx]
				i = 0
				while i < weight:
					item = queue.get()
					item.start = last_pkt_end
					item.end = item.start + TRANSMISSION_DELAY
					last_pkt_end = item.end
					self.host_map[idx].add_pkt(item)
					i += 1
			if queue.empty():
				lst.remove(elem)
				self.host_map[idx].TAT = last_pkt_end
				self.host_map[idx].throughput = last_pkt_end*1.0/len(self.host_map[idx].processed_pkts)
			count += 1

	def fq(self):
		lst  = [1,2,3,4]
		for i in range(len(lst))
			queue =  self.map[i+1]
			host = self.host_map[i+1]
			last_pkt_end = 0
			while not queue.empty():
				item = queue.get()
				item.start = last_pkt_end
				item.end = item.start + TRANSMISSION_DELAY*0.25
				last_pkt_end = item.end
				host.add_pkt(item)
			host.TAT = last_pkt_end
			host.throughput = last_pkt_end*1.0/len(host.processed_pkts)

	def wfq(self, weights):
		lst  = [1,2,3,4]
		total_weight = sum(weights)
		for i in range(len(lst))
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
			host.throughput = last_pkt_end*1.0/len(host.processed_pkts)