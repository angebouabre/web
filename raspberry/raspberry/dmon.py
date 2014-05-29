#!/usr/bin/python
import time
import subprocess
import nmap
from datetime import datetime

def check_service():
    while True:
        data="\n"
        print("It works...")
        nm = nmap.PortScanner()
        nm.scan(hosts="192.168.1.0/24", arguments='-sP')
        # a = subprocess.check_output(["nmap","-sP","192.168.1.0/24"])
        # print a
        hosts_list = [(ip, nm[ip]['status']['state'], nm[ip]['hostname']) for ip in nm.all_hosts()]
        for host, status, hostname in hosts_list:
            if status == 'up':
                res = subprocess.check_output(["arp","-a",host])
                res = str(res)
                if len(res.split(':')) > 5:
                    mac1 = res.split(':')[0][-2:]
                    mac2 = res.split(':')[1][0:10]
                    mac3 = res.split(':')[2][0:10]
                    mac4 = res.split(':')[3][0:10]
                    mac5 = res.split(':')[4][0:10]
                    mac6 = res.split(':')[5][:2]
                    mac = "%s:%s:%s:%s:%s:%s" %(mac1, mac2, mac3, mac4, mac5, mac6)
                else:
                    mac = None
                data = data + "MAC_ADDRESS=%s\nIP_ADDRESS=%s\nSTATUS=%s\n\n" %(mac, host, status)
        f = open("/home/bouable/esigetel/web/raspberry/raspberry/info.txt",'w')
        now = datetime.now()
        h = "DERNIER_NMAP=%s\n" %str(now)
        f.write(h)
        f = open("/home/bouable/esigetel/web/raspberry/raspberry/info.txt",'a')
        f.write(data)
        f.close()
        time.sleep(15)
check_service()
