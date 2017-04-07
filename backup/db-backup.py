#!/usr/bin/env python

import os
import time
import getpass

def dump():
        timestamp = time.strftime('%Y-%m-%d-%I:%M')

        print "Enter user:"
        user = raw_input()

        print "Password: "
        password = getpass.getpass()

        print "Enter host:"
        host = raw_input()

        print "Enter database name:"
        database = raw_input()

        os.popen("mysqldump -u %s -p%s -h %s %s | gzip > %s.gz" % (user,password,host,database,database+"_"+timestamp))
        print "\nDump file in "+database+"_"+timestamp+".gz"

if __name__=="__main__":
    dump()
