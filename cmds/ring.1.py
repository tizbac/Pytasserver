# -*- coding: utf-8 -*-
####RING username
###Description
##Sent by client to server when trying to play a "ring" sound to user 'username'. Only privileged users can ring anyone, although "normal" clients can ring only when they are hosting and only players participating in their battle.

if len(args) == 2:
  ri = False
  if cl.battle in self.main.battles:
    if cl.username == self.main.battles[cl.battle].founder:
      if args[1].lower() in self.main.clientsusernames:
	self.main.clientsusernames[args[1].lower()].send("RING %s\n" % cl.username)
	ri = True
  if not ri and cl.mod == 1:
    if args[1].lower() in self.main.clientsusernames:
      self.main.clientsusernames[args[1].lower()].send("RING %s\n" % cl.username)