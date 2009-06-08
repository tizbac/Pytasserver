# -*- coding: utf-8 -*-
if cl.admin == 1:
  uname = str(cl.username)
  for h in self.main.handlers:
    for kl in dict(h.clients):
      h.remove(kl,"KILLALL Command issued by %s" % uname)
      