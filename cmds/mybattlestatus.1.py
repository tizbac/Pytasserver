#print len(args)
if len(args) == 3:
  cl.setbattlestatus(args[1])
  cl.teamcolor = args[2]
  self.main.broadcastbattle(cl.battle,"CLIENTBATTLESTATUS "+cl.username+" "+cl.getbattlestatus()+" "+cl.teamcolor+"\n")