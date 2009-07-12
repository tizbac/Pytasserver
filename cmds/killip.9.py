# -*- coding: utf-8 -*-
####KILLIP mode ip/regex
##Mode can be "regex" or "normal"
Failed = False
if cl.admin == 1:
  if len(args) == 3:
    if args[1].lower() == "regex":
      try:
	tmpre = re.compile(args[2])
      except:
	c.send("SERVERMSG Regex failed to compile!\n")
	Failed = True
      if not Failed:
	for h in self.main.handlers:
	  for kl in dict(h.clients):
	    kl2 = h.clients[kl]
	    if tmpre.match(kl2.ip[0]):
	      c.send("SERVERMSG Killing username <%s> by ip\n" % kl2.username)
	      h.remove(kl,"Quit")
	      
    elif args[1].lower() == "normal":
      if not Failed:
	for h in self.main.handlers:
	  for kl in dict(h.clients):
	    kl2 = h.clients[kl]
	    if args[2] == kl2.ip[0]:
	      c.send("SERVERMSG Killing username <%s> by ip\n" % kl2.username)
	      h.remove(kl,"Quit")
  else:
    c.send("SERVERMSG Wrong number of arguments\n")
else:
  c.send("SERVERMSG Not enough rights to use that command\n")