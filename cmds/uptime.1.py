# -*- coding: utf-8 -*-
ups = int(time.time() - self.main.starttime)
u_seconds = ups % 60;
u_minutes = (( ups - ( ups % 60 ) ) / 60) % 60;
u_hours = (( ups - ( ups % 3600 ) ) / 3600) % 24;
u_days = ( ups - ( ups % 86400 ) ) / 86400;
c.send("SERVERMSG Server's uptime is %i days, %i hours, %i minutes, %i seconds\n" % (u_days,u_hours,u_minutes,u_seconds))