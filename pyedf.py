#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct

class Edf:

	def __init__(self, file_name):
		fp = open(file_name, "rb")
		self.fp = fp

		self.versioin = fp.read(8).strip()
		self.patient_id = fp.read(80).strip()
		self.recording_id = fp.read(80).strip()
		self.startdate = fp.read(8).strip()
		self.starttime = fp.read(8).strip()
		self.header_bytes = int(fp.read(8))
		self.reserved = fp.read(44)
		self.num_records = int(fp.read(8))
		self.duration = float(fp.read(8))
		self.num_signals = int(fp.read(4))
		
		self.label         = []
		self.transducer    = []
		self.phy_dim       = []
		self.phy_min       = []
		self.phy_max       = []
		self.dig_min       = []
		self.dig_max       = []
		self.pre_filtering = []
		self.nr            = []
		self.reserved2     = []

		fields = [(self.label         , 16, str.strip),
                  (self.transducer    , 80, str.strip),
                  (self.phy_dim       , 8 , str.strip),
                  (self.phy_min       , 8 , float),
                  (self.phy_max       , 8 , float),
                  (self.dig_min       , 8 , float),
                  (self.dig_max       , 8 , float),
                  (self.pre_filtering , 80, str.strip),
                  (self.nr            , 8 , int),
                  (self.reserved2     , 32, str.strip)]

		for field in fields:
			for i in range(self.num_signals):
				field[0].append(field[2](fp.read(field[1])))
		
	def read(self, record = 1):

		signals = [[] for i in range(self.num_signals)]

		for r in range(record):
			for s in range(self.num_signals):
				signals[s].extend(list(struct.unpack('h' * self.nr[s], self.fp.read(2 * self.nr[s]))))

		return signals

	def close(self):
		self.fp.close()
