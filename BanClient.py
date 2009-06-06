# -*- coding: utf-8 -*-
import socket
import thread
import string
import threading
import time
from colors import *
class BanClient:
  def ipisbanned(self,ip):
    if self.connected:
      self.lock.acquire()
      try:
	self.sock.send("IP %s\n" % ip )
	data = ""
	while not data.endswith("\n"):
	  g = self.sock.recv(1024)
	  if len(g) == 0:
	    raise socket.error
	  data += g
      except socket.error:
	bad("Connection to ban list server lost, reconnecting")
	thread.start_new_thread(self.reconnectth,())
	self.lock.release()
	return False
      response = data.upper().strip("\r\t\n ")
      if response == "OK":
	self.lock.release()
	return False
      elif response == "BANNED":
	debug("IP %s is banned from ban list server" % ip)
	self.lock.release()
	return True
      else:
	error("Unexcepted response from ban list server: '%s'" % response)
	return True
  def reconnectth(self):
    self.connected = False
    if self.reconnecting: return
    self.reconnecting = True
    
    while 1:
      try:
	notice("Trying to connect to ban list server at %s:%i..." % (self.host,self.port))
	self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	self.sock.connect((self.host,self.port))
	self.sock.settimeout(3.0)
	break
      except socket.error:
	error("Connection to ban list server failed, retrying in 2 seconds...")
	time.sleep(2)
    good("Connection to ban list server succesful")
    self.connected = True
    self.reconnecting = False
  def __init__(self,host,port):
    self.lock = threading.Lock()
    self.host = host
    self.port = port
    self.connected = False
    self.reconnecting = False
    thread.start_new_thread(self.reconnectth,())
	