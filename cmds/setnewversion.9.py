# -*- coding: utf-8 -*-
if len(args) >= 2:
  self.main.conf["springversion"] = args[1]
  self.main.writesettings()
  uname = str(cl.username)
  for h in self.main.handlers:
    for kl in dict(h.clients):
      h.remove(kl,"SETNEWVERSION Command issued by %s" % uname)