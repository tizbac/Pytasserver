# -*- coding: utf-8 -*-
####CHANNELINFO channel
###Description
##Gives informations about the channel like ChanServ !info command with SERVERMSG
if len(args) >= 2 and args[1] in self.main.channels:
  cha = self.main.channels[args[1]]
  c.send("SERVERMSG Channel #%s: Founder is <%s>\n" % (args[1],self.main.getaccountbyid(cha.founder)))
  for o in cha.operators:
    ops += self.main.getaccountbyid(int(o))+', '
  c.send("SERVERMSG Channel #%s: Operators are : %s\n" % (args[1],ops))
