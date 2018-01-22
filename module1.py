# *-* coding:utf-8 *-*

import os, re
from collections import OrderedDict

# projet P-ALES
# M2 IdL 2017-2018
# Anays Micolod & Célia Marion

# manque encore le cas des affriquées !

def extractPaires(repIn,repOut):
	'''
		fonction qui extrait les paires de phonèmes et leurs fréquences pour chaque lexique phonétisé
		rep : chaine de caractères - le repertoire contenant les lexiques phonétisés
	'''
	
	# instanciation des variables
	dicoPaires = {}
	listeP=[]
	if not os.path.isdir(repOut):
		os.mkdir(repOut)
	
	try:
		files=os.listdir(repIn)#on obtient la liste des fichiers du répertoire
	except OSError as e:
		("err n "+str(e.errno)+" lors de la lecture du dossier")
		return False
	
	#on ouvre les lexiques un à un
	for fichier in files:
		try:
			lexPho = open(repIn+"\\"+fichier,"r",encoding='utf8')
			#on récupère la langue dans le nom des fichiers (caractères avant _) 
			m=re.search(r'(.*)([_].*)',fichier)
			langue=m.group(1)
			#parcours du lexique phonétisé
			for line in lexPho:
				mot,phono=line.split("\t")
				print ("le mot "+mot+" se prononce "+phono)
				for i in range(0,len(phono)-1):
					# on traite l'élément courant (1er élément de la paire)
					if (phono[i]=='ɔ' or phono[i]=='ɑ' or phono[i]=='ɛ') and (phono[i+1]=='̃'):# cas voyelles nasales en deux caractères
						courant = phono[i]+phono[i+1]
						i+=1
					elif phono[i]!='̃':# cas normal
						courant = phono[i]
					# on traite l'élément suivant (2ème élément de la paire)
					if (phono[i+1]=='ɔ' or phono[i+1]=='ɑ' or phono[i+1]=='ɛ') and (phono[i+2]=='̃'):# pour les voyelles nasales (2 caractères en API)
						suivant=phono[i+1]+phono[i+2]
						i+=1
					elif phono[i+1]!='\n':# on vérifie qu'il y a bien un élément suivant (et pas la fin de la ligne)
						suivant = phono[i+1]
					# on forme les paires
					paire = courant+suivant
					phoneme = courant
					# ajout de la paire au dictionnaire
					if (paire not in dicoPaires.keys()):#si la paire ne figure pas encore dans le dictionnaire
						dicoPaires[paire] = 1# ajout de la paire dans en clé + fréquence=1
					else: 
						dicoPaires[paire] +=1# incrémentation de la fréquence
					if courant not in listeP:
						listeP.append(courant)
			lexPho.close()
		except IOError as e:
			print ("err n "+str(e.errno)+" lors de la lecture")
		# on stocke la liste des phonèmes dans un fichier spécifique
		try:
			#création du fichier contenant tous les phonèmes
			outputName=repOut+"\\"+langue+"_phonemes.txt"
			ficPhonemes=open(outputName,mode="w",encoding="utf8")
			for phoneme in listeP:
				ficPhonemes.write(phoneme+"\n")
		except IOError as e:
			print ("err n "+str(e.errno)+" lors de l'écriture des fichiers de phonèmes")
	del(listeP[:])
	try:
		# création du fichier d'écriture du fichier de sortie
		monFichier=open("pairesAdj.txt","w",encoding='utf8')
		# on trie le dictionnaire contenant toutes les paires par valeur (fréquence) (reverse pour tri décroissant)
		dicoPairesO=OrderedDict(sorted(dicoPaires.items(),key=lambda t:t[1], reverse=True))
		for key,value in dicoPairesO.items():
			monFichier.write("{0}\t{1}\n".format(key, value))
			# ~ print ("paire {0} (fréquence : {1})".format(key, value))
		monFichier.close()
	except IOError as e:
		print ("err n "+str(e.errno)+" lors de l'écriture des fichiers de paires")

rep=os.getcwd()
repIn=rep+"\\lexiques"
print(repIn)
repOut=rep+"\\phonemes"
print(repOut)
extractPaires(repIn,repOut)


