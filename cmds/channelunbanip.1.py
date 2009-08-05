# -*- coding: utf-8 -*-
if args[1] not in self.main.channels:
  raise CommandError("No such channel: "+args[1])
chan = self.main.channels[args[1]]
if not ( cl.accountid in chan.operators or cl.accountid == chan.founder or cl.mod == 1):
  raise CommandError("Not enough privileges")
if not self.main.ipregex.match(args[2]):
  raise CommandError("Invalid IP")
ip = args[2]
if not ip in chan.ipbans:
  raise CommandError("IP %s is not banned" % ip )
del chan.ipbans[ip]
self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has been ip-unbanned by <%s>\n" % (cl.username,args[1],ip))
chan.sync(self.main.database)