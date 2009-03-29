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
import gzip
s = socket(AF_INET,SOCK_STREAM)
def recth():
  while 1:
    data = sock.recv(1024)
    sys.stdout.write(data)
    sys.stdout.flush()
class compressedsocket:
  def __init__(self,sock):
    self.sock = sock
    self.fdw = os.fdopen(sock.fileno(),'wb')
    self.fdr = os.fdopen(sock.fileno(),'rb')
    self.gzfW = gzip.GzipFile(mode='wb', fileobj=self.fdw)
    self.gzfR = gzip.GzipFile(mode='r', fileobj=self.fdr)
  def send(self,data):
    self.gzfW.write(data)
    self.gzfW.flush()
  def recv(self,sz):
    return self.gzfR.read(sz)
  def fileno(self):
    return self.sock.fileno()
s.connect(("localhost",8205))
sock = compressedsocket(s)
thread.start_new_thread(recth,())
while 1:
  f = raw_input()
  sock.send(f+"\n")
