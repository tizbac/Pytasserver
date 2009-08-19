# -*- coding: utf-8 -*-
####SETSCRIPTTAGS key1 {value1} key2 {value2} ...
###Description
##Sent by client (battle host), to set script tags in script.txt. Keys may not contain spaces, and are expected to use the '/' character to separate tables (see example). In version 0.35 of TASServer command UPDATEBATTLEDETAILS was completely replaced by this command. The list of attributes that were replaced (with example usage):

##    * SETSCRIPTTAGS GAME/StartMetal=1000
##    * SETSCRIPTTAGS GAME/StartEnergy=1000
##    * SETSCRIPTTAGS GAME/MaxUnits=500
##    * SETSCRIPTTAGS GAME/StartPosType=1
##    * SETSCRIPTTAGS GAME/GameMode=0
##    * SETSCRIPTTAGS GAME/LimitDGun=1
##    * SETSCRIPTTAGS GAME/DiminishingMMs=0
##    * SETSCRIPTTAGS GAME/GhostedBuildings=1

##Though in reality all tags are joined together in a single SETSCRIPTTAGS command. Note that when specifying multiple key+value pairs, they must be separated by TAB characters. See the examples bellow.

###Examples
##SETSCRIPTTAG GAME/MODOPTIONS/TEST=true
##SETSCRIPTTAG GAME/StartMetal=1000 GAME/StartEnergy=1000
##See whitespaces: SETSCRIPTTAG GAME/StartMetal[SPACE]1000[TAB]GAME/StartEnergy[SPACE]1000

if len(args) >= 2:
  args2 = ' '.join(args[1:]).split("\t")
  for b in list(self.main.battles.keys()):
    if cl.username == self.main.battles[b].founder:
      for a in args2:
	bn = a.split("=")
	if len(bn) < 2:
	  continue
	tagname = bn[0].lower()
	tagvalue = '='.join(bn[1:])
	if len(bn) == 2 and len(self.main.battles[b].scripttags) < 129:
	  self.main.battles[b].scripttags[tagname] = tagvalue
	  #print self.main.battles[b].scripttags
      sts = ""
      stl = []
      for tag in self.main.battles[b].scripttags:
	stl.append(tag+"="+self.main.battles[b].scripttags[tag])
      sts = '\t'.join(stl)
      self.main.broadcastbattle(b,"SETSCRIPTTAGS %s\n" % sts)