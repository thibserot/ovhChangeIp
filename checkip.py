#!/usr/bin/python
# -*- coding: utf-8 -*-
import ovh,re,sys,os.path,getopt

def showHelp():
    print "usage:",sys.argv[0],
    print "[-h] [-o output_dir] [-v] [-d] [-i ip]"
    print "-h : Show this menu"
    print "-o : Specify the output directory to load config file"
    print "-v : Verbose mode"
    print "-d : Debug mode"
    print "-i : manually specify the ip"
    sys.exit()



args = sys.argv[1:]
optlist, args = getopt.getopt(args,"i::o::hvd")

username = ""
password = ""
output_dir = "./"
verbose = 0
debug = 0
ip = ""

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
    elif param == "-i":
        ip = val


ovh.init(output_dir,verbose,debug)

if ip == "":
    ip = ovh.get_my_ip_address()

oldip = ""
if os.path.exists(ovh.IP_PATH):
    f = open(ovh.IP_PATH,"r")
    oldip = f.read().strip()
    f.close()


if not re.search("^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$",ip):
    print "Incorrect ip address",ip
    sys.exit()
else:
    if ip != oldip:
        print "New ip is :",ip
        f = open(ovh.IP_PATH,"w")
        f.write(ip)
        f.close()
        [accounts,usernames] = ovh.loadConfig()
        for account in accounts:
            username = account["username"]
            password = account["password"]
            domains = ovh.login(username,password)
            if domains == -1:
                print "Wrong username or password", username
                continue
            else:
                domains = set(domains)
                for d in account["domains"]:
                    if not d in domains:
                        print d,"is not managed by",username
                    else:
                        ovh.selectDomain(d)
                        A = ovh.checkCurrentIp(d)
                        ovh.changeIp(d,ip,A)
                ovh.logout()

