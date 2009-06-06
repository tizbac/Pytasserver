# -*- coding: utf-8 -*-
import thread
import time
import socket
import re
import threading

banlist = []
b = open("ipbans.txt","r")
for l in b.read().split("\n"):
  if len(l) > 0:
    banlist.append(re.compile(l))
b.close()
def cth(s):
  try:
    while 1:
      data = ""
      while not data.endswith("\n"):
	data += s.recv(1024)
      commands = data.split("\n")
      for cmd in commands:
	args = cmd.strip(" \t\r\n").split(" ")
	if args[0] == "IP" and len(args) == 2:
	  h = False
	  for b in banlist:
	    if b.match(args[1]):
	      s.send("BANNED\n")
	      h = True
	      break
	  if not h:
	    s.send("OK\n")
	    
  except:
    try:
      s.close()
    except:
      pass
ms = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ms.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR,ms.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1 )
ms.bind(("127.0.0.1",8777))
ms.listen(5)
while 1:
  cs,ip = ms.accept()
  thread.start_new_thread(cth,(cs,))