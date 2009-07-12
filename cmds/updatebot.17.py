# -*- coding: utf-8 -*-
####UPDATEBOT name battlestatus teamcolor
###Description
##Sent by client when he is trying to update status of one of his own bots (only bot owner and battle host may update bot).

##battlestatus: Similar to that of the normal client's, see MYBATTLESTATUS for more info.

##teamcolor: Should be 32-bit signed integer in decimal system (e.g. 255 and not FF) where each color channel should occupy 1 byte (e.g. in hexdecimal: $00BBGGRR, B = blue, G = green, R = red).

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
	  c.send("SERVERMSG You cannot update bots if you are not the owner and you are not the host\n")
      else:
	c.send("SERVERMSG Bot doesn't exist in battle\n")
    else:
      c.send("SERVERMSG Critical Error: Your account has an invalid battle id, this is usually caused by server problems, relogin to fix it\n")
  else:
    c.send("SERVERMSG You cannot update bots if you aren't in a battle or hosting\n")