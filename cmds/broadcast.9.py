# -*- coding: utf-8 -*-
if cl.admin == 1:
  if len(args) >= 2:
    self.main.broadcast("BROADCAST %s\n" % ' '.join(args[1:]))
    