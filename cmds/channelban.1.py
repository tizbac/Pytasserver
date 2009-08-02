# -*- coding: utf-8 -*-
if len(args) > 3:
  
  if not args[1] in self.main.channels:
    raise CommandError("Channel %s doesn't exist"% args[1])
  if not args[2].lower() in self.main.clientsusernames:
    raise CommandError("No such user: %s"% args[2])
  #if not args[2] in self.main.channels[args[1]].users: # it's better being able to mute/ban also who isn't in the channel >:D
  #  raise CommandError("The specified user is not in the channel")
  if not (cl.accountid in self.main.channels[args[1]].operators or cl.accountid == self.main.channels[args[1]].founder or cl.mod == 1):
    raise CommandError("You cannot use that command on that context")
  try:
    secs = float(args[3])*60.0
  except:
    raise CommandError("Invalid ban time")
  muteip = len(args) > 4 and args[4].lower() == "ip"
  chan = self.main.channels[args[1]]
  targetclient = self.main.getuserist(args[2])
  if muteip:
    chan.ipbans.update([(targetclient.ip[0],time.time()+secs)])
    self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has ip-banned from channel <%s>\n"%(args[1],cl.username,args[2]))
  else:
    self.main.broadcastchannel(args[1],"CHANNELMESSAGE %s <%s> has account-banned from channel <%s>\n"%(args[1],cl.username,args[2]))
    chan.accountbans.update([(int(targetclient.accountid),time.time()+secs)])
  chan.sync(self.main.database)