#!/usr/bin/env python3
import time
import re
import sys
from pyvirtualdisplay import Display
from selenium import webdriver
import subprocess
def provision(ip):
    x=ip
    print("Autoprovision Click: %s" % x)

    display = Display(visible=0, size=(1920,1080))
    display.start()

    browser = webdriver.Firefox()
    browser.get('http://'+x+'/servlet?p=login&q=loginForm&jumpto=status')
    title = browser.title
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
    time.sleep(2)

    browser.get('http://'+x+'/servlet?p=settings-autop&q=load&now=true')
    time.sleep(2)
    browser.save_screenshot('page.png')
    if browser.title == "Yealink CP960 Phone":
        x = browser.find_elements_by_xpath("//*[contains(text(), 'Autoprovision Now')]")
        x[0].click()
    else:
        try:
            browser.find_element_by_name("btnAutopNow").click()
        except:
            browser.find_element_by_id("btnAutopNow").click()

    time.sleep(1)
    try:
        alert = browser.switch_to_alert()
        #print(alert.text)
        alert.accept()
    except:
        print("no alert to accept")
    time.sleep(2)
    browser.save_screenshot('page.png')
    browser.quit()
    display.stop()

if len(sys.argv) == 2:
    provision(sys.argv[1])
    quit()


cmd = ["asterisk", "-rx", "sip show peers"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
phones=[]
for line in proc.stdout.readlines():
    line = line.decode("utf-8")
    try:
        pat = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        IP=str(pat[0])
        phones.append(IP)
    except:
        pass

for x in phones:
    provision(x)
