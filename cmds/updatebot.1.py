# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
if len(args) == 4:
  if cl.battle != -1:
    if cl.battle in self.main.battles:
      ba = self.main.battles[cl.battle]
      if args[1] in ba.bots:
	if ba.bots[args[1]].owner == cl.username or ba.founder == cl.username:
	  if args[2].isdigit() and args[3].isdigit():
	    ba.bots[args[1]].update(int(args[2]),int(args[3]))
	    self.main.broadcastbattle(cl.battle,ba.bots[args[1]].forgeupdatebot(cl.battle))
	  else:
	    c.send("SERVERMSG Invalid values on UPDATEBOT command\n")
	else:
	  c.send("SERVERMSG You cannot remove bots if you are not the owner and you are not the host\n")
      else:
	c.send("SERVERMSG Bot doesn't exist in battle\n")
    else:
      c.send("SERVERMSG Critical Error: Your account has an invalid battle id, this is usually caused by server problems, relogin to fix it\n")
  else:
    c.send("SERVERMSG You cannot remove bots if you aren't in a battle or hosting\n")