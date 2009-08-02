# -*- coding: utf-8 -*-
####SAYEX channame {message}
###Description
##Sent by any client when he is trying to say something in "/me" irc style. Also see SAY command. 
if self.main.sql:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users:
    chk= self.main.channels[args[1]].checkmuted(cl)
    if chk[0]:
      c.send("CHANNELMESSAGE %s %s\n"%(args[1],chk[1]))
      raise CommandError("Cannot talk on that channel")
    self.main.broadcastchannel(args[1],"SAIDEX %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))
else:
  if len(args) >= 3 and args[1] in self.main.channels and cl.username in self.main.channels[args[1]].users:
    
    chk= self.main.channels[args[1]].checkmuted(cl)
    if chk[0]:
      c.send("CHANNELMESSAGE %s %s\n"%(args[1],chk[1]))
      raise CommandError("Cannot talk on that channel")
    self.main.broadcastchannel(args[1],"SAIDEX %s %s %s\n" % (args[1],cl.username,' '.join(args[2:])))