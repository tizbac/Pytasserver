print args
if len(args) == 3 and cl.lgstatus == 0 and self.main.sql:
  self.main.database.query("SELECT id,name FROM users WHERE name = '%s' LIMIT 1" % ( args[1].replace("'","").lower()))
  res = self.main.database.store_result()
  if res.num_rows() == 0:
    self.main.database.query("INSERT INTO users (name,password,playtime,accesslevel,bot,banned,casename) VALUES ('%s','%s',0,1,0,0,'%s')" %
    (args[1].replace("'","").lower(),args[2].replace("'",""),args[1].replace("'","")),False)
    c.send("REGISTRATIONACCEPTED\n")
  else:
    c.send("REGISTRATIONDENIED User already exists\n")
    self.remove(co,"Bad register command")
