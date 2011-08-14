#!/usr/bin/python
# -*- coding: utf-8 -*-
import ovh,os.path,urllib2,urllib,codecs,time,cookielib,re,sys,getpass,getopt

def showHelp():
    print "usage:",sys.argv[0],
    print "[-h] [-u username] [-p password]"
    sys.exit()



args = sys.argv[1:]
optlist, args = getopt.getopt(args,"u::p::h")

username = ""
password = ""

for opt in optlist:
    [param,val] = opt
    if param == "-u":
        username = val
    elif param == "-p":
        password = val
    elif param == "-h":
        showHelp()


#adding = True
#
#while adding:

while username == "":
    password = ""
    username = raw_input("Enter your OVH login :")

if password == "":
    password = getpass.getpass("Password :")
    password2 = getpass.getpass("Re-type :")
    if password != password2:
        print "password mismatch"
        sys.exit()


print [username,password]
domains = ovh.login(username,password)
if domains == -1:
    print "Wrong username or password"
    sys.exit()


account = {"username" : username,"password" : password}

account["domains"] = set()

if len(domains) == 0:
    print "There are no domains linked to this account"
    sys.exit()
elif len(domains) == 1:
    print "Monitoring :",domains[0]
    account["domains"].add(domains[0])
else:
    while (len(account["domains"]) != len(domains)):
        print "Which domain do you want to keep updated ?"
        i = 1
        for domain in domains:
            print str(i) + ")",domain
            i = i + 1
        print str(i) + ") All"
        d = -1
        while d < 1 or d > len(domains)+1:
            d = raw_input("Select the domain to monitore :")
            if not d.isdigit():
                d = -1
            else:
                d = int(d)
        d = d-1
        if d == len(domains):
            print "Monitoring every domains in this account"
            for d in domains:
                account["domains"].add(d)
        else:
            account["domains"].add(domains[d])
            print "Monitoring :",domain

        #Do you want to add another domain?
        if (len(account["domains"]) == len(domains)):
            break
        if not ovh.yes_no_question("Would you like to add another domain?"):
            break

saveConfig(account)

#if os.path.isfile(ovh.CONFIGFILE):
#    print "You already have configured the script"
#    sys.exit()
#    
#login = raw_input("Enter your OVH login :")
#password = getpass.getpass("Password :")
#password2 = getpass.getpass("Re-type :")
#if password != password2:
#    print "password mismatch"
#    sys.exit()
#
#
#print [login,password]


