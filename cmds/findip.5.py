# -*- coding: utf-8 -*-
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
	      c.send("SERVERMSG IP %s is bound to<%s>\n" % (args[2],kl2.username))
	      
    elif args[1].lower() == "normal":
      if not Failed:
	for h in self.main.handlers:
	  for kl in dict(h.clients):
	    kl2 = h.clients[kl]
	    if args[2] == kl2.ip[0]:
	      c.send("SERVERMSG IP %s is bound to <%s>\n" % (args[2],kl2.username))
  else:
    c.send("SERVERMSG Wrong number of arguments\n")
else:
  c.send("SERVERMSG Not enough rights to use that command\n")