#!/usr/bin/python3

import os
import sys
import json
import argparse
import logging
import urllib
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# Parse command line args
parser = argparse.ArgumentParser(description='Crawl by site')
parser.add_argument('-I','--iterations', metavar='N', type=int, default=3,
                    help='number or iterations')
parser.add_argument('-w','--wait', metavar='N', type=int, default=1,
                    help='wait (sec) before http request')
parser.add_argument('-s','--store', metavar='filename', default='urldict.json',
                    help='name of dictionary file')
parser.add_argument('-S','--scheme', metavar='scheme', default='http',
                    help='scheme, http or https')
parser.add_argument('-l','--log', metavar='logname', default='test.log',
                    help='name of log file')
parser.add_argument('-D','--driver', metavar='filename', default='/usr/local/bin/operadriver',
                    help='name Selenium webdriver file')
parser.add_argument('site', metavar='sitename',default='localhost',
                    help='name of processed site')

args = parser.parse_args()

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-12s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename=os.fspath(args.log),
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

log = logging.getLogger('')
log.info("Config variables site=%s,store=%s,iterations=%d,wait=%d,log=%s",args.site,args.store,args.iterations,
        args.wait,args.log)

# Start browser
webdriver_service = service.Service(os.fspath(args.driver))
webdriver_service.start()

driver = webdriver.Remote(webdriver_service.service_url, webdriver.DesiredCapabilities.OPERA)

# Init counters and variables 
cnt=0
cntwr=0
delay=args.wait

site=str(args.site)
site2='www.' + site
scheme=args.scheme
baseurl=scheme  + '://' + site

log.debug("Crawl site %s",baseurl)

urldict={} # Dictionry of urls
vspurldict={} # Additional dictionry of urls
urldict['']={'url': baseurl}

# Init stop regexp to exclude captcha, mailto etc
myre = re.compile ( "replytocom=[0-9]+" )
myre2 = re.compile ( "^mailto:" )

# Main cycle
for k in range(args.iterations):
    log.info("Iteration %d, dictionry contain %d values %d bytes", k, len(urldict), sys.getsizeof(urldict))
    vspurldict={} # Free temporary dictionry
    
    for i in urldict.keys():
        try:
            myurl=urldict[i]['url']
            if myre2.search(myurl):
                try:
                    urldict[i]['qcnt']=8
                    log.debug("Block key '%s' as email",i)
                except:
                    log.error("Cant set qcnt for key '%s'",i)

            q=urllib.parse.urlsplit(myurl)
            if myre.search(q.query):
                try:
                    log.debug("Block key '%s' as comment writing",i)
                    urldict[i]['qcnt']=9
                except:
                    log.error("Cant set qcnt for key '%s'",i)

            try:
                mycnt=urldict[i]['qcnt']
            except:
                urldict[i]['qcnt']=0
                mycnt=0
    
            if mycnt==0:
                cnt+=1
                time.sleep(delay)
                # print('Time:',time.asctime(time.localtime(time.time())),", request",cnt,", url",myurl)
                log.info("Request N=%d url=%s", cnt, myurl)
                driver.get(myurl)
                urldict[i]['url']=driver.current_url
                # urldict[i]['time']=int(time.time)
                try:
                    urldict[i]['qcnt']+=1
                except:
                    urldict[i]['qcnt']=1
    
                html_doc=driver.page_source
                soup = BeautifulSoup(html_doc, 'html.parser')
                for link in soup.find_all('a'):
                    mytxt=link.get('href')
                    mysplit=urllib.parse.urlsplit(mytxt)
                    if mysplit.netloc=='' or mysplit.netloc==site or mysplit.netloc==site2:
                        addkey=mysplit.path
                        if mysplit.query:
                            addkey=addkey + '?' + mysplit.query
                        addurl=urllib.parse.urljoin(scheme + '://' + site, mytxt)
                        log.debug("Add urldict[%s]=%s", addkey, addurl)
                        try:
                            vspurldict[addkey]['url']=addurl
                        except:
                            vspurldict[addkey]={'url': addurl,'qcnt': 0}

    
        except:
            log.error("Wrong structure for key '%s'",i)
    
    log.info("After %d, auxillary dictionry contain %d values %d bytes", k, len(vspurldict), sys.getsizeof(vspurldict))
    for i in vspurldict.keys():
        try:
            urldict[i]['url']=vspurldict[i]['url']
#             urldict[i]['qcnt']=vspurldict[i]['qcnt']
        except:
            urldict[i]=vspurldict[i]

#     
    f = open( os.fspath(args.store), 'w+')
    f.write(json.dumps(urldict, indent=4, sort_keys=True))
    f.close()

log.info("End crawling after %d requests", cnt)

# Print results

print("===========================================")
print("Cookies:",driver.get_cookies())

driver.quit() # Close browser

log.info("Print URL dictionry contain %d values %d bytes", len(urldict), sys.getsizeof(urldict))
for i in sorted(urldict.keys()):
    try:
        myurl=urldict[i]['url']
        try:
            mycnt=urldict[i]['qcnt']
        except:
            urldict[i]['qcnt']=0
            mycnt=0

        print(myurl,"requestet",mycnt,"times # key",i)
    except:
        log.error("Wrong structure for key '%s'",i)

log.info("Program end")
