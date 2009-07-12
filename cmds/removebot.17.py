# -*- coding: utf-8 -*-
####REMOVEBOT name
###Description
##Removes a bot from the battle.

if len(args) == 2:
  if cl.battle != -1:
    if cl.battle in self.main.battles:
      ba = self.main.battles[cl.battle]
      if args[1] in ba.bots:
	if ba.bots[args[1]].owner == cl.username or ba.founder == cl.username:
	  del ba.bots[args[1]]
	  self.main.broadcastbattle(cl.battle,"REMOVEBOT %i %s\n" % (cl.battle,args[1]))
	else:
	  c.send("SERVERMSG You cannot remove bots if you are not the owner and you are not the host\n")
      else:
	c.send("SERVERMSG Bot doesn't exist in battle\n")
    else:
      c.send("SERVERMSG Critical Error: Your account has an invalid battle id, this is usually caused by server problems, relogin to fix it\n")
  else:
    c.send("SERVERMSG You cannot remove bots if you aren't in a battle or hosting\n")