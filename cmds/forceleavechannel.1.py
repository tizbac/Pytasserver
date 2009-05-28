# -*- coding: utf-8 -*-
if len(args) >= 3:
  if args[1] in self.main.channels:
    if str(cl.accountid) in self.main.channels[args[1]].operators or cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1:
      if args[2].lower() in self.main.clientsusernames:
	if args[2] in self.main.channels[args[1]].users:
	  tu = self.main.allclients[self.main.clientsusernames[args[2].lower()].sck]
	  if tu != self.main.channels[args[1]].founder:
	    self.main.channels[args[1]].users.remove(args[2])
	    if len(args) > 3:
	      reason = ' '.join(args[3:])
	    else:
	      reason = "Not given"
	    self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has kicked <%s> from the channel (Reason : %s)\n" % (args[1],cl.username,tu.username,reason))
	    tu.sso.send("FORCELEAVECHANNEL %s %s %s\n" % (args[1],cl.username,reason))
	    self.main.broadcastchannel(args[1],"LEFT %s %s %s\n" % (args[1],tu.username,"Kicked from channel by %s" % cl.username))
	  else:
	    c.send("SERVERMSG %s\n" % ("Error: You cannot kick from channel the founder"))
	else:
	  c.send("SERVERMSG %s\n" % ("Error: User <%s> not in channel" % args[2]))
      else:
	c.send("SERVERMSG %s\n" % ("Error: User <%s> does not exist" % args[2]))
    else:
      c.send("SERVERMSG %s\n" % ("Error: Not enugh rights to use that command"))
  else:
    c.send("SERVERMSG %s\n" % ("Error: Channel #%s does not exist" % args[1]))
	    