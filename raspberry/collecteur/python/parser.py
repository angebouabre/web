#!/usr/bin/env python2.7
#-*-coding:utf-8-*-

import os, json, shutil
import sqlite3
import subprocess




def alert_mail(capteur, temp):
	# Import smtplib for the actual sending function
	import smtplib

	# Import the email modules we'll need
	from email.mime.text import MIMEText

	# Open a plain text file for reading.  For this example, assume that
	# the text file contains only ASCII characters.
	#fp = open(textfile, 'rb')
	# Create a text/plain message
	msg = MIMEText("Attention!!! La Temperature du %s est de %s." %(capteur, temp))
	#fp.close()

	me = "alerte.raspberry.esigetel@gmail.com"
	you = "angebouabre@gmail.com; nnengue.arno@gmail.com; alioubafr@gmail.com"
	msg['Subject'] = '***Alerte température du %s***' % capteur
	msg['From'] = "Raspberry" 
	msg['To'] = you

	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP("smtp.gmail.com", 587)
	s.ehlo()
	s.starttls()
	s.ehlo

	s.login(me,"Esigetel1")
	s.sendmail(me, [you], msg.as_string())
	s.quit()







def get_last_pk(db):
    conn  = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select id from moniteur_mesure order by id")
    val = c.fetchall()
    val = val[-1][0]
    return val

#Connexion a la carte et récuperation des données qu'on stocke dans un fichier en local dans /home/pi/data/



try:
    a = subprocess.call(["bash","/home/bouable/esigetel/web/raspberry/collecteur/bash/download.sh"])
except:
    pass



#On recupère le dernier id des mesures
bdd = "/home/bouable/esigetel/web/raspberry/mesure.db"
pk = get_last_pk(bdd)
pk += 1

#On parcours les fichiers du dossier des données et on les parse
doss = "/home/pi/data"
for fic in os.listdir(doss):
    if "hygrometrie" in fic:
        opened = open(os.path.join(doss,fic))
        for line in opened:
            print line
            if "Hum" in line:
                hum = line.split("=")[2].replace("%","").replace(" ", "")
                date = fic.split("_")[4] + "-" + fic.split("_")[3] + "-" + fic.split("_")[2] + " " + fic.split("_")[5] +\
                ":" + fic.split("_")[6].replace(".txt","")+":00"
		fields = {"fields":{"date_mesure":date, "valeur":float(hum), "capteur":["capteur4"]}, "model":"moniteur.mesure", "pk":pk}
                pk += 1
		fields = json.dumps(fields)
		data = '[' + fields + ']'
		if not os.path.isdir("/home/pi/fixture"):
		    os.makedirs("/home/pi/fixture")

                date = fic.split("_")[4] + "-" + fic.split("_")[3] + "-" + fic.split("_")[2] + " " + fic.split("_")[5] +\
                ":" + fic.split("_")[6].replace(".txt","")+":00"

		output_file = "/home/pi/fixture/hygro_du_%s.json" %date.replace(" ","_").replace(":","_")

		f = open(output_file, 'w')
		f.write(data)
		f.close()
    else:
	    opened = open(os.path.join(doss,fic))
	    for line in opened:
		if "t=" in line:
		    line = line.split("=")
		    temperature = float(line[-1])/1000
		    date =  fic.split("_")[5] + "-" + fic.split("_")[4] + "-" + fic.split("_")[3] + " " + fic.split("_")[6] +\
		    ":" + fic.split("_")[7].replace(".txt","")+":00"
		    print date
		    id_capt = fic.split("_")[2]
		    if  id_capt == "28-000005d305e4":
			fields = {"fields":{"date_mesure":date, "valeur":temperature, "capteur":["capteur1"]}, "model":"moniteur.mesure", "pk":pk}
			#if temperature < 20:
			#    temperature = str(temperature)
			#    alert_mail("capteur 1", temperature) 
		    elif id_capt == "28-000005d31e24":
			fields = {"fields":{"date_mesure":date, "valeur":temperature, "capteur":["capteur2"]}, "model":"moniteur.mesure", "pk":pk}
			#if temperature < 20:
			#    temperature = str(temperature)
			#    alert_mail("capteur 1", temperature) 

		    elif id_capt == "28-000002ad9190":
			fields = {"fields":{"date_mesure":date, "valeur":temperature, "capteur":["capteur3"]}, "model":"moniteur.mesure", "pk":pk}
			#if temperature < 20:
			#    temperature = str(temperature)
			#    alert_mail("capteur 1", temperature) 
		    pk += 1 
		    
		    fields = json.dumps(fields)
		    data = '[' + fields + ']'

		    if not os.path.isdir("/home/pi/fixture"):
			os.makedirs("/home/pi/fixture")

		    date =  fic.split("_")[5] + "-" + fic.split("_")[4] + "-" + fic.split("_")[3] + " " + fic.split("_")[6] +\
		    ":" + fic.split("_")[7].replace(".txt","")+":00"

		    output_file = "/home/pi/fixture/temperature_du_%s.json" %date.replace(" ","_").replace(":","_")

		    f = open(output_file, 'w')
		    f.write(data)
		    f.close()
#On crée un nouveau fichier dans le dossier fixture
		    print "succes:", output_file, "généré."

#On injecte les données dans la bdd
#try:
subprocess.call(["bash","/home/bouable/esigetel/web/raspberry/collecteur/bash/loaddata.sh"])
#except:
#    print "ici" 
#On supprime le repertoire complet de la fixture
print "succes:", output_file, "sauvergardé dans la bdd."
shutil.rmtree("/home/pi/fixture")
shutil.rmtree(doss)
os.makedirs(doss)
