# -*- coding: utf-8 -*-
####JOINBATTLE BATTLE_ID [password]
###Description
##Sent by a client trying to join a battle. Password is an optional parameter.
if len(args) < 2:
  c.send("JOINBATTLEFAILED Error: Not enough arguments\n" )
  raise CommandError("Not enough arguments")
battleid = int(args[1])
battle = self.main.battles[battleid]
if battle.locked == 1:
  c.send("JOINBATTLEFAILED Error: Battle is locked\n" )
  raise CommandError("Battle is locked")
if battle.passworded == 1:
  if len(args) >= 3:
    if battle.password != ' '.join(args[2:]):
      c.send("JOINBATTLEFAILED Error: Invalid password\n" )
      raise CommandError("Invalid Password")
  else:
    c.send("JOINBATTLEFAILED Error: No password specified\n" )
    raise CommandError("No password specified")
battle.players.append(cl.username)
c.send("JOINBATTLE %i %s\n" % (battleid,battle.hashcode))
self.main.broadcast("JOINEDBATTLE %i %s\n" % (battleid,cl.username))
cl.battle = battleid
for p in list(battle.players):
  if p != cl.username:
    GT = self.main.allclients[self.main.clientsusernames[p.lower()].sck]
    c.send("CLIENTBATTLESTATUS %s %s %s\n" % (p,GT.getbattlestatus(),GT.teamcolor))
c.send("REQUESTBATTLESTATUS\n")
botsaf = dict(battle.bots)
uts = []
for u in battle.disabledunits:
  uts.append(u)
  if len(uts) >= 30:
    c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
    uts = []
if len(uts) > 0:
  c.send("DISABLEUNITS %s\n" % (' '.join(uts)))
for bot_ in botsaf:
  bot = botsaf[bot_]
  c.send(bot.forgeaddbot(int(battleid)))
for rect in dict(battle.startrects):
  r = battle.startrects[rect]
  c.send(r.forgeaddstartrect())
stl=[]
for tag in battle.scripttags:
  stl.append(tag+"="+battle.scripttags[tag])
sts = '\t'.join(stl)
c.send("SETSCRIPTTAGS %s\n" % sts)
if int(battle.type) == 1:
  c.send("SCRIPTSTART\n")
  for l in battle.replayscript:
    c.send("SCRIPT %s\n" % l)
  c.send("SCRIPTEND\n")
