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
  def send(self,data):
    self.sock.send(zlib.compress(data))
  def recv(self,sz):
    return zlib.decompress(self.sock.recv(sz))
  def fileno(self):
    return self.sock.fileno()
s.connect(("localhost",8205))
sock = compressedsocket(s)
thread.start_new_thread(recth,())
while 1:
  f = raw_input()
  sock.send(f+"\n")
