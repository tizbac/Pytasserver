from socket import *
import string
import thread
import time
import sys
import traceback
import pdb
import os
import re
import select
import base64
from cStringIO import StringIO
import md5
import commands
from ParseConfig import *
from colors import *
import zlib
s = socket(AF_INET,SOCK_STREAM)
def recth():
  while 1:
    data = sock.recv(1024)
    sys.stdout.write(data)
    sys.stdout.flush()
class compressedsocket:
  def __init__(self,sock):
    self.sock = sock
    self.tx = 0
    self.rx = 0
    self.txc = 0
    self.rxc = 0
    self.co = zlib.compressobj(9)
    self.sock.send(self.co.flush(zlib.Z_SYNC_FLUSH))
    self.dc = zlib.decompressobj()
  def send(self,data):
    self.tx += len(data)
    self.co.compress(data)
    cdata = self.co.flush(zlib.Z_SYNC_FLUSH)
    self.txc += len(cdata)
    self.sock.send(cdata)
    
  def recv(self,sz):
    
    data = self.sock.recv(sz)
    if data == "":
	return ""
    #debug("Compressed: "+data.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue))
    self.rxc += len(data)
    datau = self.dc.decompress(data)
    self.rx += len(datau)
    debug("UNCompressed: "+datau.replace("\n",red+"\\n"+blue).replace("\r",red+"\\r"+blue))
    if datau == "":
	datau = "\n"
    return datau
  def fileno(self):
    return self.sock.fileno()


s.connect((sys.argv[1],8205))
sock = compressedsocket(s)
thread.start_new_thread(recth,())
try:
	while 1:
	  f = raw_input()
	  sock.send(f+"\n")
except KeyboardInterrupt:
	print "TX Compression : %f , RX Compression : %f" % (float(sock.txc)/float(sock.tx)*100.0,float(sock.rxc)/float(sock.rx)*100.0)
