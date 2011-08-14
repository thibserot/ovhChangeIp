#!/usr/bin/python
# -*- coding: utf-8 -*-
import ovh,os.path,urllib2,urllib,codecs,time,cookielib,re,sys,getopt

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


adding = True
[accounts,usernames] = ovh.loadConfig()
ovh.showAccounts(accounts)

while adding:
        #What do you want to do?
        d = ""
        while not d.isdigit() or int(d) < 1 or int(d) > 5:
            print "What do you want to do?"
            print "1) Add another account"
            print "2) Edit the current account"
            print "3) Delete an account"
            print "4) List accounts"
            print "5) I'm done thank you"
            d = raw_input("Enter your choice : ")
        d = int(d)

        if d == 1:
            print "Creating a new account"
            res = ovh.getLogin(username,password)
            if res == -1:
                continue
            else:
                [username,password] = res
                if username in usernames:
                    print "Username already managed.Please choose Edit"
                    continue
                account = ovh.createAccount(username,password)
                if account != -1 and len(account["domains"]) > 0:
                    # Adding the set
                    accounts += [account,]
                    usernames.add(account["username"])
        elif d == 2:
            print "Editing an account"
            if len(accounts) == 0:
                print "No account to edit yet.Please Add an account first"
                continue
            else:
                print "Which account would you like to edit?"
                i = 1
                for account in accounts:
                    print str(i)+")",account["username"]
                    for domain in account["domains"]:
                        print "\t",domain
                    i = i + 1
                d = ""
                while not d.isdigit() or int(d) < 1 or int(d) > len(accounts):
                    d = raw_input("Account #: ")
                print "Editing account",d
                d = int(d) - 1
        elif d == 3:
            print "Deleting an account"
            if len(accounts) == 0:
                print "No account to delete.Please Add an account first"
                continue
            else:
                print "Which account would you like to delete?"
                i = 1
                for account in accounts:
                    print str(i)+")",account["username"]
                    for domain in account["domains"]:
                        print "\t",domain
                    i = i + 1
                d = ""
                while not d.isdigit() or int(d) < 1 or int(d) > len(accounts):
                    d = raw_input("Account #:" )
                print "Deleting account",d
                d = int(d) - 1
                usernames.remove(accounts[d]["username"])
                accounts = accounts[:d] + accounts[d+1:]
        elif d == 4:
            print "Listing accounts"
            ovh.showAccounts(accounts)
        else:
            break
        username = ""
        password = ""
        

ovh.saveConfig(accounts)

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


