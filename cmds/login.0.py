
if len(args) >= 5 and cl.lgstatus < 1 and args[1] not in self.main.clientsusernames.keys():
  if self.main.sql:
    self.main.database.query("SELECT name,password,playtime,accesslevel,bot,banned,casename,id FROM users WHERE name = '%s' AND password = '%s' LIMIT 1" % (args[1].replace("'","").lower(),args[2].replace("'","")))
    res = self.main.database.store_result()
    if res.num_rows() >= 1:
      r2 = res.fetch_row()[0]
      cl.username = r2[6]
      cl.accountid =int(r2[7])
      cl.password = r2[1]
      cl.ptime = int(r2[2])
      cl.bot = int(r2[4])
      if int(r2[3]) >= 2:
	cl.mod = 1
      if int(r2[3]) >= 3:
	cl.admin = 1
      c.send("ACCEPTED %s\n" % cl.username)
      motd = "Hi %s! Welcome to pytasserver\n %i Connected players in %i opened battles" % ( cl.username,len(self.main.clientsusernames.keys()),len(self.main.battles))
      for l in motd.split("\n"):
	c.send("MOTD %s\n" % l)
      self.main.clientsusernames.update([(cl.username,c)])
      self.main.clientsaccid.update([(cl.accountid,c)])
      self.main.broadcast("ADDUSER %s %s %i\n" % (cl.username,cl.country,cl.cpu))
      cl.lgstatus = 1
      
      allclients = dict(self.main.allclients)
      for c2 in allclients:
	cl2 = allclients[c2]
	if cl2.lgstatus >= 1:
	  c.send("ADDUSER %s %s %i\n" % (cl2.username,cl2.country,cl2.cpu))
	  newstatus = cl2.getstatus()
	  c.send("CLIENTSTATUS %s %i\n" % (cl2.username,newstatus))
      c.send("LOGININFOEND\n")

    else:
      #print str(args)+" LOGIN failed"
      c.send("DENIED %s\n" % ("Bad username/password"))
      #self.remove(co,"Bad login attempt")
      
  else:
    cl.username = args[1]
    cl.password = args[2]
    try:
      cl.cpu = int(args[3])
    except:
      cl.cpu = 0
    c.send("ACCEPTED %s\n" % cl.username)
    motd = "Hi %s! Welcom to pytasserver\n %i Connected players in %i opened battles" % ( args[1],len(allusernames),len(self.main.battles))
    for l in motd.split("\n"):
      c.send("MOTD %s\n" % l)
    self.main.clientsusernames.update([(cl.username,c)])
    self.main.broadcast("ADDUSER %s %s %i\n" % (cl.username,cl.country,cl.cpu))
    cl.lgstatus = 1
    
    #allclients = dict()
    #for h in self.main.handlers:
    #  for k in dict(h.clients):
	#allclients.update([(k,h.clients[k])])
    for c2 in dict(self.main.allclients):
      cl2 = self.main.allclients[c2]
      if cl2.lgstatus >= 1:
	  c.send("ADDUSER %s %s %i\n" % (cl2.username,cl2.country,cl2.cpu))
	  newstatus = cl2.getstatus()
	  c.send("CLIENTSTATUS %s %i\n" % (cl2.username,newstatus))
    c.send("LOGININFOEND\n")
elif len(args) >= 5 and cl.lgstatus < 1 and cl.username in self.main.clientsusernames.keys():
  c.send("DENIED %s\n" % ("Already logged in"))
  self.remove(co,"Bad login attempt")
else:
  self.remove(co,"Bad data")