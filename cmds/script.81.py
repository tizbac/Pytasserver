# -*- coding: utf-8 -*-
if len(args) > 1:
  if len(self.main.battles[cl.battleid].replayscript) < 200:
    self.main.battles[cl.battleid].replayscript.append(' '.join(args[1:]))
  else:
    raise CommandError("You have exceeded maximum replayscript length")
else:
  raise CommandError("Not enough arguments")