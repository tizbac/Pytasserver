# -*- coding: utf-8 -*-
def getrank(status):
	bit0 = (status >> 2) & 1
	bit1 = (status >> 3) & 1
	bit2 = (status >> 4) & 1
	rank = 1*bit0+2*bit1+2*2*bit2
	return rank
def getmod(status):
	return (status >> 5) & 1
def getaway(status):
	return (status >> 1) & 1
def getingame(status):
	return (status >> 0) & 1
def getbot(status):
	return (status >> 6) & 1
def getready(status):
	return (status >> 1) & 1
def getready(status):
	return (status >> 1) & 1
def getteam(status):
	bit0 = (status >> 2) & 1
	bit1 = (status >> 3) & 1
	bit2 = (status >> 4) & 1
	bit3 = (status >> 5) & 1
	team = 1*bit0+2*bit1+2*2*bit2+2*2*2*bit3
	return team
def getally(status):
	bit0 = (status >> 6) & 1
	bit1 = (status >> 7) & 1
	bit2 = (status >> 8) & 1
	bit3 = (status >> 9) & 1
	team = 1*bit0+2*bit1+2*2*bit2+2*2*2*bit3
	return team
def getspec(status):
	return (status >> 10) & 1
def gethand(status):
	bit0 = (status >> 11) & 1
	bit1 = (status >> 12) & 1
	bit2 = (status >> 13) & 1
	bit3 = (status >> 14) & 1
	bit4 = (status >> 15) & 1
	bit5 = (status >> 16) & 1
	bit6 = (status >> 17) & 1
	hand = pow(2,0)*bit0+pow(2,1)*bit1+pow(2,2)*bit2+pow(2,3)*bit3+pow(2,4)*bit4+pow(2,5)*bit5+pow(2,6)*bit6+pow(2,7)*bit4
	return hand
def getsync(status):
	bit0 = (status >> 22) & 1
	bit1 = (status >> 23) & 1
	sync = 1*bit0+2*bit1
	return sync
def getside(status):
	bit0 = (status >> 24) & 1
	bit1 = (status >> 25) & 1
	bit2 = (status >> 26) & 1
	bit3 = (status >> 27) & 1
	side = 1*bit0+2*bit1+2*2*bit2+2*2*2*bit3
	return side
def getcolor(status):
	r = float((status >> 0) & 255)/255.0
	g = float((status >> 8) & 255)/255.0
	b  = float((status >> 16) & 255)/255.0
	return r,g,b
def reverse(chars):
		ochars = ''
		beyond = len(chars)
		for ix in range(beyond):
			ochars += chars[beyond - 1 - ix]
		return ochars

def bin2dec(s):
	return int(reverse(s), 2)

def dec2bin(i, bits=None):
	i = int(i)
	b = ''
	while i > 0:
		j = i & 1
		b = str(j) + b
		i >>= 1
	if bits:
		b = b.rjust(bits,'0')
	return reverse(b)
def dec2bin_2(i, bits=None):
	i = int(i)
	b = ''
	while i > 0:
		j = i & 1
		b = str(j) + b
		i >>= 1
	if bits:
		b = b.rjust(bits,'0')
	return b