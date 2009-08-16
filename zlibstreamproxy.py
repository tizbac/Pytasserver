# -*- coding: utf-8 -*-
import socket
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
	datau = ""
    return datau
  def fileno(self):
    return self.sock.fileno()
  def close(self):
    self.sock.close()
    self.sock.shutdown(SHUT_RDWR)
def clientthreadsend(sock,csock):
  data = ""
  while 1:
    while 1:
      try:
	data = sock.recv(1024)
	break
      except socket.error:
	if str(sys.exc_value[0]) != "timed out":
	  data = ""
	  break
	
    if len(data) == 0:
      print "Closing sockets"
      print "TX Compression Ratio: %f , RX Compression Ratio: %f" % (float(csock.txc)/float(csock.tx)*100.0,float(csock.rxc)/float(csock.rx)*100.0)
      try:
	sock.close()
      except:
	pass
      try:
	csock.close()
      except:
	pass
      break
    try:
      csock.send(data)
    except:
      print "Closing sockets"
      print "TX Compression Ratio: %f , RX Compression Ratio: %f" % (float(csock.txc)/float(csock.tx)*100.0,float(csock.rxc)/float(csock.rx)*100.0)
      try:
	sock.close()
      except:
	pass
      try:
	csock.close()
      except:
	pass
      break
  print "Thread exited"
def clientthreadrecv(sock,csock):
  data = ""
  while 1:
    try:
      print "Reading comressed socket"
      while 1:
	try:
	  data = csock.recv(1024)
	  break
	except socket.error:
	  if str(sys.exc_value[0]) != "timed out":
	    data = ""
	    break
      print "Read done"
    except socket.error:
      data = ""
    if len(data) == 0:
      print "Closing sockets"
      print "TX Compression Ratio: %f , RX Compression Ratio: %f" % (float(csock.txc)/float(csock.tx)*100.0,float(csock.rxc)/float(csock.rx)*100.0)
      try:
	sock.close()
      except:
	pass
      try:
	csock.close()
      except:
	pass
      break
    try:
      sock.send(data)
    except:
      print "Closing sockets"
      print "TX Compression Ratio: %f , RX Compression Ratio: %f" % (float(csock.txc)/float(csock.tx)*100.0,float(csock.rxc)/float(csock.rx)*100.0)
      try:
	sock.close()
      except:
	pass
      try:
	csock.close()
      except:
	pass
      break
  print "Thread exited"
ms = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ms.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
ms.bind(("localhost",8201))

ms.listen(5)
while 1:
  cs,ip = ms.accept()
  connsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  connsock.connect((sys.argv[1],8205))
  zs = compressedsocket(connsock)
  cs.settimeout(5)
  zs.sock.settimeout(5)
  thread.start_new_thread(clientthreadsend,(cs,zs))
  thread.start_new_thread(clientthreadrecv,(cs,zs))