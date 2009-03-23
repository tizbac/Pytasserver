try:
  cl.afk = getaway(int(args[1]))
  cl.ingame = getingame(int(args[1]))
  newstatus = cl.getstatus()
  self.main.broadcast("CLIENTSTATUS %s %i\n" % (cl.username,newstatus))
except:
  bad("Invalid clientstatus from "+cl.username)