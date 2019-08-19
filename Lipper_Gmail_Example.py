
# coding: utf-8

# In[5]:

import schedule
import time, os
import smtplib
import datetime    
import requests
from bs4 import BeautifulSoup
import os, certifi
import ftplib
import urllib2, ssl
Path =  #Path where you would like the daily download of folds
url = 'http://lipperftp.thomsonreuters.com' 
username = #Lipper_username
password = #Lipper_password
Time = "17:58" # When to run script, 24 hour clock. 
os.chdir(Path)



gmail_user = #gmail_username
gmail_password = #gmail_pass

sent_from = gmail_user 
to = [gmail_user]  
subject = 'Lipper Script is Down'  
body = 'Lipper Script is Down'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


# In[6]:

def lipper_job():
    certifi.old_where()
    d = datetime.date.today()
    os.chdir(Path)
    if not os.path.isdir(str(d.year) +"_"+ str(d.month)+"_"+str(d.day)):
        os.mkdir(str(d.year) +"_"+ str(d.month)+"_"+str(d.day))
    newdir = Path + '\\'+str(d.year) +'_'+ str(d.month)+'_'+str(d.day)
    os.chdir(newdir)
    ftp=ftplib.FTP()
    ftp.connect('lipperftp.thomsonreuters.com',21)
    ftp.login('hedgeworld_st','LipperHedge')
    ftp.retrlines('LIST')
    filenames = ftp.nlst()
    for filename in filenames:
        host_file = os.path.join(newdir, filename)
        try:
            with open(host_file, 'wb') as local_file:
                ftp.retrbinary('RETR %s' % filename, local_file.write) #Download in filename in binary transfer mode to local file
        except ftplib.error_perm:
            pass

schedule.every().day.at(Time).do(lipper_job)

keep_going=True

while keep_going:
	try:
		schedule.run_pending()
		time.sleep(1)
	except Exception as e:
		server = smtplib.SMTP_SSL("smtp.gmail.com",465) 
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, email_text)
		server.close()

		print 'Email sent!'
		print(e.message)
		keep_going=False


