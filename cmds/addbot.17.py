# -*- coding: utf-8 -*-
####ADDBOT name battlestatus teamcolor {AIDLL}
###Description
##With this command client can add bots to the battle.

##teamcolor: Should be 32-bit signed integer in decimal system (e.g. 255 and not FF) where each color channel should occupy 1 byte (e.g. in hexdecimal: $00BBGGRR, B = blue, G = green, R = red).

if len(args) >= 4:
  if cl.battle != -1:
    if cl.battle in self.main.battles:
      if len(args) > 4:
	aidll = ' '.join(args[4:])
      else:
	aidll = ""
      ba = self.main.battles[cl.battle]
      ba.bots.update([(args[1],Bot(cl.username,args[1],args[2],args[3],aidll))])
      self.main.broadcastbattle(cl.battle,ba.bots[args[1]].forgeaddbot(cl.battle))
    else:
      c.send("SERVERMSG Critical Error: Your account has an invalid battle id, this is usually caused by server problems, relogin to fix it\n")
  else:
    c.send("SERVERMSG You cannot add bots if you aren't in a battle or hosting\n")