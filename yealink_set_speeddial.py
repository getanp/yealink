#!/usr/bin/env python3
import time
import re
import sys
from pyvirtualdisplay import Display
from selenium import webdriver
import subprocess

def addDialplan(ip,prefix,replace):
    x=ip
    print("Configuring Dialplan: %s" % x)
    try:
        display = Display(visible=0, size=(1920,1080))
        display.start()
 
        browser = webdriver.Firefox()
        browser.get('http://'+x+'/servlet?p=login&q=loginForm&jumpto=status')
        old=1
        phone = browser.title
        #quit()
        try:
            if browser.title == "Yealink CP960 Phone":
                username = browser.find_element_by_name("idUsername")
                old=0
            else:
                username = browser.find_element_by_name("username")
        except:
            username = browser.find_element_by_id("idUsername")
            old=0

        try:
            if browser.title == "Yealink CP960 Phone":
                password = browser.find_element_by_name("idPassword")
                old=0
            else:
                password = browser.find_element_by_name("pwd")
        except:
            password = browser.find_element_by_id("idPassword")
            old=0

        username.send_keys("admin")
        password.send_keys("admin")
        browser.find_element_by_id("idConfirm").click()
        time.sleep(1)
        #browser.save_screenshot('page.png')

        uri="servlet?m=mod_data&p=settings-dialplan&q=load"
        if old == 0:
            uri="servlet?m=mod_data&p=settings-dialplan&q=load"

        browser.get('http://'+x+"/"+uri)
        #time.sleep(1)
        #print('http://'+x+"/"+uri)
        #browser.save_screenshot('page.png')

        editPrefix = browser.find_element_by_name("editPrefix")
        editReplace = browser.find_element_by_name("editReplace")
        account = browser.find_element_by_name("editAccount")
        editPrefix.send_keys(prefix)
        editReplace.send_keys(replace)
        account.send_keys("1")
        try:
            browser.find_element_by_name("addreplacerule").click()
        except:
            if browser.title == "Yealink CP960 Phone":
                x = browser.find_elements_by_xpath("//*[contains(text(), 'Add')]")
                x[0].click()
            else:
                browser.find_element_by_id("addreplacerule").click()


        browser.save_screenshot('page.png')
        browser.quit()
        display.stop()
    except Exception as e:
        print("Failed: %s" % e)


if len(sys.argv) == 4:
    addDialplan(sys.argv[1], sys.argv[2], sys.argv[3])
    quit()

#cmd = ["asterisk", "-rx", "sip show peers"]
#proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
#phones=[]
#for line in proc.stdout.readlines():
#    line = line.decode("utf-8")
#    try:
#        pat = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
#        IP=str(pat[0])
#        phones.append(IP)
#    except:
#        pass

#for x in phones:
#    addDialPlan(x)
