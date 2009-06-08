# -*- coding: utf-8 -*-
if cl.admin == 1:
  if len(args) >= 3:
    if args[1].lower() in self.main.clientsusernames:
      self.main.clientsusernames[args[1].lower()].send(' '.join(args[2:])+"\n")