#!/usr/bin/python


import os, sys   

path = os.path.abspath('..')
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "raspberry.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


import time
import subprocess
import nmap
from datetime import datetime
from moniteur.models import Carte 

cur =  os.getcwd()
nmap_info_file = cur+"/info.txt"

print nmap_info_file

def check_service():
    while True:
        data="\n"
        cartes = []
        print("Scanning Network...")
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
                    carte = Carte.objects.get(mac=mac)
                    carte.status = status
                    macs = cartes.append(mac)
                    carte.save()
                else:
                    mac = None
                data = data + "HOSTNAME=%s\nMAC_ADDRESS=%s\nIP_ADDRESS=%s\nSTATUS=%s\n\n" %(hostname, mac, host, status)
        f = open(nmap_info_file,'w')
        now = datetime.now()
        h = "DERNIER_NMAP=%s\n" %str(now)
        f.write(h)
        f = open(nmap_info_file,'a')
        f.write(data)
        f.close()
        cartes = Carte.objects.exclude(mac__in=cartes)
        for carte in cartes:
            carte.status = "Down"
            carte.save()
        time.sleep(10)
check_service()
