# -*- coding: utf-8 -*-
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