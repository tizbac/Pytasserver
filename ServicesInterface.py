# -*- coding: utf-8 -*-
#This works in binary mode
import socket
import string
import struct
from struct import *
import time
import thread
import threading
import pickle
import sys
import traceback
from colors import *
#Server->Client
OP_CONNECTED = 0x01 #No args
OP_CLIENTCONNECTED = 0x02# Client IP (4x char) , Services ID (unsigned short)
OP_CLIENTDISCONNECTED = 0x03# Services ID, string tag(name : reason) reason
OP_CLIENTSENT = 0x04# Services ID,string tag(name : data) data
OP_CHANNELOPENED = 0x05# Channelname string tag name 0x01
OP_CHANNELCLOSED = 0x06# Channelname string tag name 0x01
OP_BATTLEOPENED = 0x07# Battle ID(unsigned short)
OP_BATTLECLOSED = 0x08# Battle ID(unsigned short)
OP_CLIENTLOGGEDIN = 0x09# Services ID, string tag username(name 0x01)
OP_PONG = 0x0A# No args
OP_CLIENTJOINEDCHANNEL = 0x0B#Services ID,ChannelName
OP_CLIENTLEFTCHANNEL =0x0C#Services ID,ChannelName
OP_RESULT = 0x0D# result tag
OP_ERROR = 0xff #Last command failed , args(desc)

#Client->Server
OP_GETCLIENTATTR = 0x01# Services ID, attrname ( sring tag) in class Client
OP_KILLCLIENT = 0x02# Services ID, reason
OP_BROADCAST = 0x03# data
OP_BROADCASTCHANNEL = 0x04#Channelname , data
OP_BROADCASTBATTLE = 0x05#BattleID , data
OP_SETCLIENTATTR = 0x06#Services ID, attrname ( sring tag) in class Client,value( tag type is also important)
OP_FORGEMSG = 0x07#Services ID , data
OP_EXECPYTHON = 0x08#Execs in services context
OP_PING = 0x09#No args
def rawip(ip):
  data = ""
  i= ip.split(".")
  data += chr(int(i[0]))+chr(int(i[1]))+chr(int(i[2]))+chr(int(i[3]))
  return data
def createpacket(opcode,data):
  pkt = ""
  pkt += struct.pack("IH",len(data),opcode)
  pkt += data
  return pkt
def parsepacket(data):
  if len(data) >= 6:
    size,opcode = struct.unpack("IH",data[:6])
    
  else:
    return (0x00,"",data)   #(opcode,data,remainingdata)
  if len(data[6:]) >= size:
    return (opcode,data[6:6+size],data[6+size:])
def forgetag(name,value):#Taken from ed2k protocol implementation
  types = { str : 2 , float : 4 , int : 3 }
  data = ""
  data += chr(types[type(value)])
  if type(name) == str:
    data += pack("H",len(name))
    data += name
  else:
    data += pack("H",1)
    data += chr(name)
  if type(value) == str:
    data += pack("H",len(value))
    data += value
  elif type(value) == float:
    data += pack("f",value)
  elif type(value) == int:
    data += pack("I",abs(value))#Crap
  return data
def parsetag(data):
  #error("parsetag : %s - Not implemented" % ( str([data])))
  if len(data) > 0:
    typ = ord(data[0])
    if (typ & 0x80):
      typ &= 0x7F
      name = ord(data[1])
    else:
      length = unpack("H",data[1:3])[0]
      if length == 1:
	name = ord(data[3])
	cl = 4
      else:
	
	name = data[3:length+3]
	cl = length+3
    if typ == 2:# String tag
      
      l2 = unpack("H",data[cl:cl+2])[0]
     # print "Str length:" + str([data[cl:cl+2]])
      value= str(data[cl+2:cl+2+l2])
      rdata = data[cl+2+l2:]
    elif typ == 3:# Integer tag
      value = unpack("I",data[cl:cl+4])[0]
      rdata = data[cl+4:]
    elif typ == 4:# Float tag
      value = unpack("f",data[cl:cl+4])[0]
      rdata = data[cl+4:]
    else:
      error("Invalid tag type: %x"%typ)
      return None
    #good("%s tag(Name: %s): %s" % ( str(type(value)),str([name]),str(value)))
    return (name,value,rdata)
  else:
    error("Parsetag: empty data")
class ServicesClient:
  def __init__(self,socket,mainist,servicesinst):
    self.sock = socket
    self.lastping = time.time()
    self.main = mainist
    self.recvbuffer = ""
    self.sendbuffer = []
    self.services = servicesinst
    self.sendpacket(OP_CONNECTED,"")
  def sendpacket(self,opcode,data):
    dt = createpacket(opcode,data)
    self.sendbuffer.append(dt)
  def onpacket(self,opcode,data):
    try:
      #print "Packet: ",opcode,[data]
      if opcode == OP_PING:
	self.lastping = time.time()
	self.sendpacket(OP_PONG,"")
      if opcode == OP_KILLCLIENT and len(data) >= 2:
	servid = struct.unpack("H",data)[0]
	target = self.services.serverclients[servid]
	if len(data) > 2:
	  reason = parsetag(data[2:])[1]
	else:
	  reason = "Killed from Services, Reason tag missing"
	for h in self.main.handlers:
	  if target in h.clients:
	    h.remove(target,reason)
	    break
      if opcode == OP_BROADCAST and len(data) > 0:
	bdata = parsetag(data)[1]
	self.main.broadcast(bdata)
      if opcode == OP_BROADCASTCHANNEL and len(data) >0:
	channeltag = parsetag(data)
	datatag = parsetag(channeltag[2])
	self.main.broadcastchannel(channeltag[1],datatag[1])
      if opcode == OP_BROADCASTBATTLE and len(data) > 2:
	battleid = struct.unpack("H",data[:2])[0]
	datatag = parsetag(data[2:])
	self.main.broadcastbattle(battleid,datatag[1])
      if opcode == OP_SETCLIENTATTR and len(data) > 2:
	servid = struct.unpack("H",data[:2])[0]
	attrnametag = parsetag(data[2:])
	valuetag = parsetag(attrnametag[2])
	exec "self.services.serverclients[servid].%s = valuetag[1]" % attrnametag[1]
      if opcode == OP_GETCLIENTATTR and len(data) > 2:
	#print "Received OP_GETCLIENTATTR"
	servid = struct.unpack("H",data[:2])[0]
	attrnametag = parsetag(data[2:])
	self.main.allclients[self.services.serverclients[servid].sso.sck]
	try:
	  exec "value = str(self.services.serverclients[servid].%s)"% attrnametag[1]
	except:
	  self.sendpacket(OP_ERROR,forgetag(0x01,str(sys.exc_value)))
	  value = ""
	self.sendpacket(OP_RESULT,forgetag("value",value))
	#print "Sent OP_RESULT"
      if opcode == OP_FORGEMSG and len(data) > 2:
	servid = struct.unpack("H",data[:2])[0]
	datatag = parsetag(data[2:])
	self.services.serverclients[servid].sso.send(datatag[1])
      if opcode == OP_EXECPYTHON and len(data) > 0:
	#print "OP_EXECPYTHON"
	try:
	  codetag = parsetag(data)
	  exec codetag[1]
	except:
	  error("While executing Services code:"+traceback.format_exc())
	  error("Code was:"+codetag[1])
	  self.sendpacket(OP_ERROR,forgetag(0x01,str(sys.exc_value)))
	  self.sendpacket(OP_RESULT,forgetag("value",""))
    except:
      self.sendpacket(OP_ERROR,forgetag(0x01,str(sys.exc_value)))
      
  def receive(self):
    try:
      data = self.sock.recv(1024)
      if len(data) == "":
	return (False,"End of stream")
      self.recvbuffer += data
    except socket.error:
      if int(sys.exc_value[0]) != 11:
	return (False,str(sys.exc_value))
    
    a = parsepacket(self.recvbuffer)
    if not a:
      return (False,"Received invalid packet")
    if a[0] != 0:
      self.recvbuffer = a[2]
      opcode = a[0]
      data = a[1]
      self.onpacket(opcode,data)
    return (True,None)
  def flush(self):
    #print time.time(),self.sendbuffer
    y = ""
    try:
      for x in list(self.sendbuffer):
	y = str(x)
	 #print "Try send "+str([y])
	self.sock.send(y)
	self.sendbuffer.remove(y)
    except:
      pass
      #print "Failed sending "+str([y])
class Services:
  def onclientcreated(self,client):
    debug("Services: onclientcreated "+str(client))
    self.serverclientslock.acquire()
    for i in range(0,65536):
      if not self.serverclients[i]:
	self.serverclients[i] = client
	self.broadcast(OP_CLIENTCONNECTED,rawip(client.ip[0])+struct.pack("H",i))
	self.serverclientsreverse[client] = i
	break
    self.serverclientslock.release()
  def onclientjoinedchannel(self,client,channame):
    self.broadcast(OP_CLIENTJOINEDCHANNEL,struct.pack("H",self.serverclientsreverse[client])+forgetag("channel",channame))
  def onclientleftchannel(self,client,channame):
    self.broadcast(OP_CLIENTLEFTCHANNEL,struct.pack("H",self.serverclientsreverse[client])+forgetag("channel",channame))  
  def onclientloggedin(self,client):
    self.broadcast(OP_CLIENTLOGGEDIN,struct.pack("H",self.serverclientsreverse[client])+forgetag(0x01,client.username)) 
  def onclientremoved(self,client,reason):
    
    self.serverclientslock.acquire()
    i = self.serverclientsreverse[client]
    self.broadcast(OP_CLIENTDISCONNECTED,struct.pack("H",i)+forgetag("reason",reason))
    self.serverclients[i] = None
    del self.serverclientsreverse[client]
    self.serverclientslock.release()
    debug("Services: onclientremoved "+str(client))
  def onclientsent(self,client,data): #Called when a client sends a line to server
    self.broadcast(OP_CLIENTSENT,struct.pack("H",self.serverclientsreverse[client])+forgetag("data",data))
 
  def broadcast(self,opcode,data):
    #print "broadcast ",[opcode,data]
    self.clientslock.acquire()
    for cs in self.clients:
      self.clients[cs].sendpacket(opcode,data)
    self.clientslock.release()
  def mainloop(self):
    clientstoremove = []
    try:
      while 1:
	
	self.clientslock.acquire()
	for cs in self.clients:
	  
	  ret = self.clients[cs].receive()
	  if not ret[0]:
	    print ret[1]
	    clientstoremove.append(cs)
	  if time.time() -self.clients[cs].lastping > 15.0:
	    print "Timeout"
	    clientstoremove.append(cs)
	  self.clients[cs].flush()
	for c in list(clientstoremove):
	  try:
	    c.close()
	  except:
	    pass
	  del self.clients[c]
	  clientstoremove.remove(c)
	self.clientslock.release()
	time.sleep(0.05)
    except:
      print traceback.format_exc()
  def acceptconnections(self):
    while 1:
      cs,ip = self.ms.accept()
      cs.setblocking(0)
      self.clientslock.acquire()
      self.clients[cs] = ServicesClient(cs,self.main,self)
      self.clientslock.release()
  def __init__(self,port,mainist,host="localhost"):
    self.main = mainist
    self.clients = dict()
    self.serverclients = dict()
    for i in range(0,65536):
      self.serverclients[i] = None
    self.serverclientsreverse = dict()
    self.clientslock = threading.Lock()
    self.serverclientslock = threading.Lock()
    self.ms = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.ms.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,self.ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
    self.ms.bind((host,port))
    self.ms.listen(5)
    thread.start_new_thread(self.acceptconnections,())
    thread.start_new_thread(self.mainloop,())
if __name__ == "__main__":
  a = Services(7000,None)
  while 1:
    time.sleep(100.0)