# -*- coding: utf-8 -*-
####SAY channame {message}
###Description
##Sent by client when he is trying to say something in a specific channel. Client must first join the channel before he can receive or send messages to that channel.

###Response
##SAID

if self.main.sql:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users:
    chk= self.main.channels[args[1]].checkmuted(cl)
    if chk[0]:
      c.send("CHANNELMESSAGE %s %s\n"%(args[1],chk[1]))
      raise CommandError("Cannot talk on that channel")
    self.main.broadcastchannel(args[1],"SAID %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))
else:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users:
    
    chk= self.main.channels[args[1]].checkmuted(cl)
    if chk[0]:
      c.send("CHANNELMESSAGE %s %s\n"%(args[1],chk[1]))
      raise CommandError("Cannot talk on that channel")
    self.main.broadcastchannel(args[1],"SAID %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))