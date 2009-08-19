# -*- coding: utf-8 -*-
####LOGIN username password cpu localIP {lobby name and version} [{userID}]	 Source: client
###Description
##Sent by client when he is trying to log on the server. Server may respond with ACCEPTED or DENIED command. Note that if client hasn't yet confirmed the server agreement, then server will send the agreement to client upon receiving LOGIN command (LOGIN command will be ignored - client should resend LOGIN command once user has agreed to the agreement or disconnect from the server if user has rejected the agreement).
##Also see LOGININFOEND command.

##password: Should be sent in encoded form (MD5 hash in base-64 form). Note that when server is running in lan mode, you can specify any username and password (password will be ignored, but you must send some string anyway - you mustn't ommit it!)

##cpu: An integer denoting the speed of client's processor in MHz (or value of x+ tag if AMD). Client should leave this value at 0 if it can't figure out its CPU speed.

##localIP: As localIP client should send his local IP (e.g. 192.168.x.y, or whatever it uses) so server can forward local IPs to clients behind same NAT (this resolves some of the host/joining issues). If client is unable to determine his local IP, he should send "*" instead.

##userID: This is a unique user identification number provided by the client-side software. It should be an unsigned integer encoded in hexadecimal form (see examples). Note that this parameter is optional - by default it is not used/set. Server will send a ACQUIREUSERID command to tell the client that he must provide a user ID, if needed. However, if client-side lobby program was using user ID before, it should send it along with LOGIN command.

###Examples
##LOGIN Johnny Gnmk1g3mcY6OWzJuM4rlMw== 3200 192.168.1.100 TASClient 0.30
##LOGIN Johnny Gnmk1g3mcY6OWzJuM4rlMw== 3200 * TASClient 0.30
##LOGIN Johnny Gnmk1g3mcY6OWzJuM4rlMw== 3200 * TASClient 0.30 FA23BB4A
success = False
if not cl.loggingin:
  cl.loggingin = True
  cl.loginlock.acquire()
try:
  r2 = None
  lanclient = False
  if len(args) < 5:
    raise CommandError("Not enough args")
  if cl.lgstatus > 0:
    raise CommandError("Already Logged in with this connection")
  if args[1].lower() in self.main.clientsusernames:
    raise CommandError("An user with that name is already logged in")
  if self.main.sql:
    self.main.database.query("SELECT name,password,playtime,accesslevel,bot,banned,casename,id FROM users WHERE name = '%s' AND password = '%s' LIMIT 1" % (self.main.database.escape(args[1]).lower(),self.main.database.escape(args[2])))
    res = self.main.database.store_result()
    if res.num_rows() > 0:
      r2 = res.fetch_row()[0]
    elif self.main.au:
      self.main.database.query("SELECT name FROM users WHERE name = '%s'" % (self.main.database.escape(args[1])))
      res2 = self.main.database.store_result()
      if res2.num_rows() != 0:
	raise CommandError("An user with that name exists in database and you used wrong password")
      else:
	lanclient = True
    else:
      raise CommandError("Invalid username / password")
  else:
    lanclient = True
    r2 = None
  val = self.main.validateusername(args[1])
  if not val[0] and not r2:
    c.send("DENIED %s\n" % val[1])
    raise CommandError("Invalid username")
  if r2:
    cl.username = r2[6]
    cl.oldname = cl.username
    cl.accountid =int(r2[7])
    cl.password = r2[1]
    cl.sql = not lanclient
    cl.ptime = int(r2[2])
    cl.bot = int(r2[4])
    cl.lastlogin = int(time.time())
    if int(r2[3]) >= 2:
      cl.mod = 1
    if int(r2[3]) >= 3:
      cl.admin = 1
    try:
      cl.cpu = int(args[3])
    except:
      cl.cpu = 0
    if self.main.ipregex.match(args[4]):
      cl.lanip = args[4]
    else:
      cl.lanip = "*"
  else:
    cl.username = args[1]
    cl.oldname = cl.username
    cl.password = args[2]
    cl.accountid = -int(time.time()*10000.0) #Hope that will not fail ;)
    cl.sql = False
    try:
      cl.cpu = int(args[3])
    except:
      cl.cpu = 0
    if self.main.ipregex.match(args[4]):
      cl.lanip = args[4]
    else:
      cl.lanip = "*"
  cl.lgstatus = 1
  c.send("ACCEPTED %s\n" % cl.username)
  good("%s Logged in (Using sql = %s )" % (cl.username,str(cl.sql)))
  allclients = dict(self.main.allclients)
  self.main.clientsusernames.update([(cl.username.lower(),c)])
  self.main.clientsaccid.update([(cl.accountid,c)])
  self.main.broadcast("ADDUSER %s %s %i\n" % (cl.username,cl.country,cl.cpu))
  self.main.broadcast("CLIENTSTATUS %s %i\n" % (cl.username,int(cl.getstatus())))
  for c2 in allclients:
    cl2 = allclients[c2]
    if cl2.lgstatus >= 1:
      c.send("ADDUSER %s %s %i\n" % (cl2.username,cl2.country,cl2.cpu))
      newstatus = cl2.getstatus()
      c.send("CLIENTSTATUS %s %i\n" % (cl2.username,newstatus))
  battles = dict(self.main.battles)
  for b2 in battles:
    c.send(battles[b2].forgebattleopened(cl))
    c.send(battles[b2].forgeupdatebattleinfo())
    for u in battles[b2].players:
      c.send("JOINEDBATTLE %i %s\n" % (int(b2),u))
  c.send("LOGININFOEND\n")
  
  if self.main.services:
    self.main.services.onclientloggedin(cl)
except CommandError:
  cl.loginlock.release()
  c.send("DENIED %s\n" % str(sys.exc_value))
  self.remove(co,"Bad login attempt")
  raise CommandError(str(sys.exc_value))
except:
	error("LOGIN")
	error(traceback.format_exc())
try:
  cl.loginlock.release()
except:
  pass
if cl.username.lower() in self.main.clientsusernames and self.main.clientsusernames[cl.username.lower()].sck not in self.clients:
	#Client got killed before login,revert login
	notice("Client killed while logging in, reverting")
	del self.main.clientsusernames[cl.username.lower()]
	if cl.accountid in self.main.clientsaccid:
		del self.main.clientsaccid[cl.accountid]
	
