#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib, sys, datetime,ovh,getopt
from email.mime.text import MIMEText

def showHelp():
    print "usage:",sys.argv[0],
    print "[-h] [-o output_dir] [-v] [-d]"
    print "-h : Show this menu"
    print "-o : Specify the output directory to load config file"
    print "-v : Verbose mode"
    print "-d : Debug mode"
    sys.exit()



args = sys.argv[1:]
optlist, args = getopt.getopt(args,"i::o::hvd")

username = ""
password = ""
output_dir = "./"
verbose = 0
debug = 0

for opt in optlist:
    [param,val] = opt
    if param == "-o":
        output_dir = val
    elif param == "-h":
        showHelp()
    elif param == "-v":
        verbose = 1
    elif param == "-d":
        debug = 1

ovh.init(output_dir,verbose,debug)

config = ovh.loadEmail()
if config == -1:
    print "No connection info to send the mail, please run the config tool first"
else:
    [username,password] = config
    val = sys.stdin.read()
    if len(val) > 2:
        msg = MIMEText(val)
        msg['Subject'] = "Updating ip address at " + str(now)
        me = username
        you = username
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login(username,password)
        s.sendmail(me,[you], msg.as_string())
        s.close()
        print "Mail sent"
