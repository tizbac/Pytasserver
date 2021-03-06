# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#This works in binary mode
import socket
import string
import struct
import time
import thread
import threading
import sys
import traceback
import select
from struct import *
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
OP_CLIENTJOINEDCHANNEL = 0x0B#Services ID,ChannelName
OP_CLIENTLEFTCHANNEL =0x0C#Services ID,ChannelName
OP_PONG = 0x0A# No args
OP_RESULT = 0x0D# result tag
OP_ERROR = 0xff #Last command failed , args(desc)

opcodesctable = {0x01 : "OP_CONNECTED", 0x02:"OP_CLIENTCONNECTED",0x03:"OP_CLIENTDISCONNECTED",0x04:"OP_CLIENTSENT",0x05:"OP_CHANNELOPENED",0x06:"OP_CHANNELCLOSED",0x07:"OP_BATTLEOPENED",0x08:"OP_BATTLECLOSED",0x09:"OP_CLIENTLOGGEDIN",0x0A:"OP_PONG",0xff:"OP_ERROR"}
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
  def broadcast(self,data):
    self.sock.send(createpacket(OP_BROADCAST,forgetag("data",data)))
  def broadcastchannel(self,channame,data):
    self.sock.send(createpacket(OP_BROADCASTCHANNEL,forgetag("channame",channame)+forgetag("data",data)))
  def forgemsg(self,clientid,data):
    self.sock.send(createpacket(OP_FORGEMSG,pack("H",clientid)+forgetag("data",data)))
  def execpython(self,code):
    self.sock.send(createpacket(OP_EXECPYTHON,forgetag("code",code)))
  def getaccountnamebyid(self,id):
    code = ""
    code += "self.sendpacket(OP_RESULT,forgetag(\"accname\",self.main.getaccountbyid(%s)))" % id
    self.execpython(code)
    return self.getresult()
  def getaccountid(self,name):
    code = ""
    code += "self.sendpacket(OP_RESULT,forgetag(\"accid\",self.main.getaccountid(\"%s\")))" % name
    self.execpython(code)
    return int(self.getresult())
  def getresult(self):
    self.returnlock.acquire()
    print "Waiting for attrname response..."
    self.returnlock.acquire()#Should lock the thread
    try:
      self.returnlock.release()
    except:
      pass
    print "Unlocked"
    return self.returnvalue
  def getclientattr(self,cid,attrname):
    
    self.sock.send(createpacket(OP_GETCLIENTATTR,pack("H",cid)+forgetag("attrname",attrname)))
    self.returnlock.acquire()
    #print "Waiting for attrname response..."
    self.returnlock.acquire()#Should lock the thread
    try:
      self.returnlock.release()
    except:
      pass
    return self.returnvalue
  def pingthread(self):
    while 1:
      try:
	self.sock.send(createpacket(OP_PING,""))
      except:
	error("Cannot ping")
      time.sleep(self.pinginterval)
  def stdinthread(self):
    tags = dict()
    while 1:
      a = raw_input(">>> ")
      b = a.split(" ")
      if b[0].lower() == "broadcast":
	data = ' '.join(b[1:])
	data += "\n"
	self.sock.send(createpacket(OP_BROADCAST,forgetag("data",data)))
      if b[0].lower() == "send":
	if len(b) >= 3:
	  data = ' '.join(b[2:])
	  for t in tags:
	    data = data.replace(t,tags[t])
	  exec "self.sock.send(createpacket(%s,data))" % b[1].upper()
      if b[0].lower() == "createtag":
	if len(b) >= 5:
	  tagvarname = b[1]
	  tagname = b[2]
	  tagtype = b[3]
	  tagvalue = b [4]
	  exec "tags[\"%s\"] = forgetag(tagname,%s(tagvalue))"%(tagvarname,tagtype)
	  print [tags[tagvarname]]
	  
  def tryreconnect(self):
    self.clients = dict()
    try:
      self.sock.close()
    except:
      pass
    while 1:
      try:
	self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	self.sock.connect((self.host,self.port))
	print "Connected"
	break
      except:
	time.sleep(10.0)
	print "Reconnect failed"
  def recvthread(self):
    while 1:
      try:
	data = self.sock.recv(1024)
	#print data
	if len(data) == 0:
	  print "EOF From Server"
	  self.tryreconnect()
	self.buf += data
      except socket.error:
	print "Reconnecting"
	self.tryreconnect()
      
  def parsethread(self):
   
    while 1:
      a = parsepacket(self.buf)
      #print a
      if not a:
	return (False,"Received invalid packet")
      if a[0] != 0:
	self.buf = a[2]
	opcode = a[0]
	data = a[1]
	#print opcode
	if opcode == OP_ERROR:
	  print "Error on server: %s" % parsetag(data)[1]
	elif opcode == OP_RESULT:
	  print "received result, unlocking lock"
	  self.returnvalue = parsetag(data)[1]
	  try:
	    self.returnlock.release()
	  except:
	    pass
	#print "Received ",opcodesctable[opcode],data
	elif opcode in self.callbacks:
	  self.callbacks[opcode](data)
      else:
	time.sleep(0.1)


  def __init__(self,host="localhost",pinginterval=10.0):
    self.host = host
    self.buf = ""
    self.clients = dict()
    self.callbacks = dict()
    self.pinginterval = pinginterval
    self.port = 7100
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.sock.connect((self.host,self.port))
    self.returnvalue = ""
    self.returnlock = threading.Lock()
    
    thread.start_new_thread(self.parsethread,())
    thread.start_new_thread(self.pingthread,())
    thread.start_new_thread(self.recvthread,())
if __name__ == "__main__":
  ist = ServicesClient()
  try:
    ist.stdinthread()
  except KeyboardInterrupt:
    ist.sock.close()
    exit()