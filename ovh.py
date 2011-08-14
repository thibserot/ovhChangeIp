#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,urllib2,urllib,codecs,time,cookielib,re,sys,pickle,getpass

OUTPUT_DIR = "./"
LOG_DIR = OUTPUT_DIR + "log/"
COOKIEFILE = OUTPUT_DIR + "cookie.lwp"
CONFIGFILE = OUTPUT_DIR + "config.ovh"
DEBUG = 1
VERBOSE = 1

urlopen = urllib2.urlopen
Request = urllib2.Request
cj = cookielib.LWPCookieJar()
if os.path.isfile(COOKIEFILE):
    cj.load(COOKIEFILE)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

lasturl = ""

if DEBUG == 1 and not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def login(user,password,encoding=""):
    if VERBOSE == 1:
        print "login as",user
    url = "https://www.ovh.com/managerv3/login.pl"
    # Authentification
    values = {  "ref":"home.pl", 
                "refxls":"", 
                "xsldoc":"sub-login.xsl",
                "time":int(time.time()),
                "domain":"",
                "ajaxScn":"",
                "ticketId":"",
                "level":"",
                "todo":"Login",
                "refererLanguage":"en",
                "language":"en",
                "session_nic":user,
                "session_password":password
             }
    htmlSource = readURL2(url,values,"post",encoding)
    if DEBUG == 1:
        f = codecs.open(LOG_DIR + "login-1.html","w",encoding='utf-8')
        f.write(htmlSource)
        f.close()

    # Check if the username is correct:
    if re.search("Wrong user id or password: Can't Login",htmlSource):
        if VERBOSE == 1:
            print "Wrong username or password"
        return -1

    if VERBOSE == 1:
        print "listing every domain available :"
    # Page with every host
    url = "https://www.ovh.com/managerv3/home.pl"
    values = {  "xsldoc":"",
                "domain":"",
                "time":int(time.time()),
                "language":"en",
                "csid":"0",
                "ticketId":"",
                "level":""
             }
    htmlSource = readURL2(url,values,"get",encoding)
    if DEBUG == 1:
        f = codecs.open(LOG_DIR + "login-2.html","w",encoding='utf-8')
        f.write(htmlSource)
        f.close()
    # Find the domain we want to edit
    domains = getAllDomain(htmlSource)
    if VERBOSE == 1:
        print domains
    return domains

def selectDomain(domain,encoding=""):
    #if len(domains) == 1:
    #    domain = domains[0]
    #else:
    #    print "can't decide which domain to choose"
    #    sys.exit()
    # Select the domain
    url = "https://www.ovh.com/managerv3/sub-home.pl"
    values = {  "xsldoc":"",
                "language":"en",
                "domain" : domain,
                "hostname" : domain,
                "service" : domain,
                "lastxsldoc" : "sub-home-hosting.xsl",
                "csid" : "0",
                "referer" : ""
             }

    htmlSource = readURL2(url,values,"get",encoding)
    if DEBUG == 1:
        f = codecs.open(LOG_DIR + "login-3.html","w",encoding='utf-8')
        f.write(htmlSource)
        f.close()

def checkCurrentIp(domain,encoding=""):
    #Go to the Domain & DNS page
    if VERBOSE == 1:
        print "going to the Domain & DNS page"
    url = "https://www.ovh.com/managerv3/hosting-domain.pl"
    values = {  "language":"en",
                "domain" : domain,
                "hostname" : domain,
                "service" : domain,
                "lastxsldoc" : "sub-home-hosting.xsl",
                "csid" : "0"
              }
    htmlSource = readURL2(url,values,"get",encoding)
    if DEBUG == 1:
        f = codecs.open(LOG_DIR + "login-4.html","w",encoding='utf-8')
        f.write(htmlSource)
        f.close()

    # Select DNS Zone
    if VERBOSE == 1:
        print "selecting DNS Zone"
    url = "https://www.ovh.com/managerv3/hosting-domain-zone.pl"
    values = {  "xsldoc":"hosting/domain/hosting-domain-zone.xsl",
                "language":"en",
                "domain" : domain,
                "hostname" : domain,
                "service" : domain,
                "lastxsldoc" : "hosting/domain/hosting-domain.xsl",
                "csid" : "0"
             }
    htmlSource = readURL2(url,values,"get",encoding)
    if DEBUG == 1:
        f = codecs.open(LOG_DIR + "login-5.html","w",encoding='utf-8')
        f.write(htmlSource)
        f.close()
    # Get every A field we have and update them one by one
    A = getAllA(htmlSource)
    if VERBOSE == 1:
        print "A subdomains available :",A
    return A

def changeIp(domain,ip,A,encoding=""):
    for a in A:
        [subdomain,target] = a
        if target == ip:
            if VERBOSE == 1:
                print subdomain,"already has the proper ip",ip
            continue
        # To remove
        if subdomain == "":
            continue
        
        if VERBOSE == 1:
            print "selecting A subdomain",subdomain,"with",target
        url = "https://www.ovh.com/managerv3/hosting-domain-zone.pl"
        values = {  "xsldoc":"hosting/domain/zoneModify.xsl",
                    "subdomain" : subdomain,
                    "fieldtype" : "A",
                    "target" : target,
                    "language":"en",
                    "domain" : domain,
                    "hostname" : domain,
                    "service" : domain,
                    "lastxsldoc" : "hosting/domain/hosting-domain-zone.xsl",
                    "csid" : "0",
                    "editMxAnyway":"1"
                 }
        htmlSource = readURL2(url,values,"get",encoding)
        if DEBUG == 1:
            f = codecs.open(LOG_DIR + "login-6.html","w",encoding='utf-8')
            f.write(htmlSource)
            f.close()
        # Modify the A field for the current subdomain
        if VERBOSE == 1:
            print "updating A subdomain",subdomain,"with",ip
        url = "https://www.ovh.com/managerv3/hosting-domain-zone.pl"
        values = {  "xsldoc":"hosting/domain/hosting-domain-zone.xsl",
                    "subdomain" : subdomain,
                    "zonesub":subdomain,
                    "fieldtype" : "A",
                    "priority" : "1",
                    "plan":"CUSTOM",
                    "target" : target,
                    "target_new" : ip,
                    "language":"en",
                    "domain" : domain,
                    "hostname" : domain,
                    "service" : domain,
                    "lastxsldoc" : "hosting/domain/zoneModify.xsl",
                    "csid" : "0",
                    "todo":"DnsEntryModifyCustom"
                 }
        htmlSource = readURL2(url,values,"get",encoding)
        if DEBUG == 1:
            f = codecs.open(LOG_DIR + "login-7 " + subdomain + ".html","w",encoding='utf-8')
            f.write(htmlSource)
            f.close()


def readURL2(url,values,method="post",encoding=""):
    global lasturl
    if lasturl == "":
        lasturl = url
    headers = {'User-agent': 'Mozilla/5.0',"Referer":lasturl}
    data = urllib.urlencode(values)
    #print data
    if method == "get":
        url = url + "?" + data
        #print url
        data= None
    req = Request(url, data,headers)


    handle = urlopen(req)
    htmlSource = handle.read()
    #print "method:",req.get_method()
    #print values
    #print handle.info()
    lasturl = url
    if encoding == "":
        encoding = handle.headers['content-type'].split('charset=')[-1]
    if encoding == "text/html":
        return htmlSource
    try:
        htmlSource = unicode(htmlSource,encoding)
    except UnicodeEncodeError:
        htmlSource = unicode(htmlSource,"latin-1")
    return htmlSource


def getAllDomain(htmlSource):
    domains = re.findall("domainChange\('([^']+)'\)",htmlSource)
    return domains

def getAllA(htmlSource):
    A = re.findall("ListAction\('hosting/domain/zoneModify.xsl', '([^']*)', 'A', '([^']*)'",htmlSource)
    return A

def yes_no_question(question =""):
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
    while True:
        choice = raw_input(question).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print "Please respond with 'yes' or 'no'"

def saveConfig(config):
    with open(CONFIGFILE,"wb") as f:
        pickle.dump(config,f)

def loadConfig():
    if os.path.exists(CONFIGFILE):
        with open(CONFIGFILE, "rb") as f:
            config = pickle.load(f)
        usernames = set()
        for c in config:
            usernames.add(c["username"])
        return [config,usernames]
    return [[],set()]

def getLogin(username,password):
    while username == "":
        password = ""
        username = raw_input("Enter your OVH login :")
    
    if password == "":
        password = getpass.getpass("Password :")
        password2 = getpass.getpass("Re-type :")
        if password != password2:
            print "password mismatch"
            return -1

    return [username,password]


def manageDomains(domains):
    accountDomains = set()
    if len(domains) == 0:
        print "There are no domains linked to this account"
    elif len(domains) == 1:
        print "Monitoring :",domains[0]
        accountDomains.add(domains[0])
    else:
        while (len(domains) > 0):
            print "Which domain do you want to keep updated ?"
            i = 1
            for domain in domains:
                print str(i) + ")",domain
                i = i + 1
            print str(i) + ") All"
            d = -1
            while not d.isdigit() or int(d) < 1 or int(d) > len(domains)+1:
                d = raw_input("Select the domain to monitore :")
            d = int(d)
            d = d-1
            if d == len(domains):
                print "Monitoring every domains in this account"
                for d in domains:
                    accountDomains.add(d)
                domains = []
            else:
                accountDomains.add(domains[d])
                print "Monitoring :",domains[d]
                domains = domains[:d] + domains[d+1:]
            #Do you want to add another domain?
            if len(domains)== 0:
                break
            if not yes_no_question("Would you like to add another domain?"):
                break
    return accountDomains


def createAccount(username,password):
    res = getLogin(username,password)
    if res == -1:
        return -1
    else:
        [username,password] = res

        domains = login(username,password)
        if domains == -1:
            print "Wrong username or password"
            username = ""
            password = ""
            return -1
        else:
            account = {"username" : username,"password" : password}
            account["domains"] = manageDomains(domains)
            return account


def showAccounts(accounts):
    if len(accounts) == 0:
        print "No account stored"
    else:
        i = 1
        for account in accounts:
            print str(i)+")",account["username"]
            for domain in account["domains"]:
                print "\t",domain
            i = i + 1
    raw_input("Press ENTER to continue...")
