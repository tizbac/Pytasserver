# -*- coding: utf-8 -*-
if len(args) > 1:
  if args[1] in self.main.channels:
    cha = self.main.channels[args[1]]
    c.send("MUTELISTBEGIN %s\n" % args[1])
    for m in cha.mutes:
      c.send("MUTELIST %s, %s\n" % (str(m),str(cha.mutes[m])))
    
    
    c.send("MUTELISTEND\n")
    