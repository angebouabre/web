#!/usr/bin/env python2.7
#-*-coding:utf-8-*-

import os, json, shutil
import sqlite3
import subprocess


def get_last_pk(db):
    conn  = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select id from moniteur_mesure order by id")
    val = c.fetchall()
    val = val[-1][0]
    return val

#Connexion a la carte et récuperation des données qu'on stocke dans un fichier en local dans /home/pi/data/
try:
    a = subprocess.call(["bash","/home/pi/bash/download.sh"])
except:
    pass

#On recupère le dernier id des mesures
bdd = "/home/pi/web/raspberry/mesure.db"
pk = get_last_pk(bdd)
pk += 1

#On parcours les fichiers du dossier des données et on les parse
doss = "/home/pi/data"
for fic in os.listdir(doss):
    opened = open(os.path.join(doss,fic))
    for line in opened:
        if "t=" in line:
            line = line.split("=")
            temperature = float(line[-1])/1000
            date =  fic.split("_")[4] + "-" + fic.split("_")[3] + "-" + fic.split("_")[2] + " " + fic.split("_")[5] +\
            ":" + fic.split("_")[6].replace(".txt","")+":00" 
            fields = {"fields":{"date_mesure":date, "valeur":temperature, "capteur":["capteur4"]}, "model":"moniteur.mesure", "pk":pk}

fields = json.dumps(fields)
data = '[' + fields + ']'

if not os.path.isdir("/home/pi/fixture"):
    os.makedirs("/home/pi/fixture")

date =  fic.split("_")[2] + "-" + fic.split("_")[3] + "-" + fic.split("_")[4] + "_" + fic.split("_")[5] +\
"_" + fic.split("_")[6].replace(".txt","") 

output_file = "/home/pi/fixture/temperature_du_%s.json" %date

f = open(output_file, 'w')
f.write(data)
f.close()
#On crée un nouveau fichier dans le dossier fixture
print "succes:", output_file, "généré."

#On injecte les données dans la bdd
#try:
subprocess.call(["bash","/home/pi/bash/loaddata.sh"])
#except:
#    print "ici" 
#On supprime le repertoire complet de la fixture
print "succes:", output_file, "sauvergardé dans la bdd."
shutil.rmtree("/home/pi/fixture")
shutil.rmtree(doss)
os.makedirs(doss)
