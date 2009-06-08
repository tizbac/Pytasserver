# -*- coding: utf-8 -*-
####MYSTATUS status
###Description
##Sent by client to server telling him his status changed. To figure out if battle is "in-game", client must check in-game status of the host.

##status: A signed integer in text form (e.g. "1234"). Each bit has its meaning:

##    * b0 = in game (0 - normal, 1 - in game)
##    * b1 = away status (0 - normal, 1 - away)
##    * b2-b4 = rank (see Account class implementation for description of rank) - client is not allowed to change rank bits himself (only server may set them).
##    * b5 = access status (tells us whether this client is a server moderator or not) - client is not allowed to change this bit himself (only server may set them).
##    * b6 = bot mode (0 - normal user, 1 - automated bot). This bit is copied from user's account and can not be changed by the client himself. Bots differ from human players in that they are fully automated and that some anti-flood limitations do not apply to them.


try:
  cl.afk = getaway(int(args[1]))
  if cl.ingame == 0 and getingame(int(args[1])) == 1:
    if cl.battle != -1:
      cl.ptimecounter = [time.time(),cl.battle]
    else:
      cl.ptimecounter = None
  if cl.ingame == 1 and getingame(int(args[1])) == 0:
    if cl.battle != -1 and cl.ptimecounter[1] == cl.battle:
      cl.ptime += int(time.time() - cl.ptimecounter[0]) / 60
    cl.ptimecounter = None
  cl.ingame = getingame(int(args[1]))
  newstatus = cl.getstatus()
  self.main.broadcast("CLIENTSTATUS %s %i\n" % (cl.username,newstatus))
except:
  bad("Invalid clientstatus from "+cl.username)