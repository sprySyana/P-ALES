# *-* coding:utf-8 *-*

import os
import re
from collections import OrderedDict

# Projet P-ALES
# M2 IdL 2017-2018
# Anays Micolod & Célia Marion

# Il manque encore le cas des affriquées

def extractPaires(repIn,repOut):
    """
    fonction qui extrait les paires de phonèmes et leurs fréquences 
        pour chaque lexique phonétisé
    repIn : string - le répertoire contenant les lexiques phonétisés
    repOut : string - le répertoire contenant les fichiers de phonèmes
    """
    # Instanciation des variables
    dicoPaires = {}
    listeP = []
    if not os.path.isdir(repOut):
        os.mkdir(repOut)
    
    try:
        # On obtient la liste des fichiers du répertoire
        files=os.listdir(repIn)
    except OSError as e:
        ("err n "+str(e.errno)+" lors de la lecture du dossier")
        return False
    
    # On ouvre les lexiques un à un
    for fichier in files:
        try:
            lexPho = open(repIn+"\\"+fichier,"r",encoding="utf8")
            # On récupère la langue dans le nom des fichiers
            m = re.search(r'(.*)([_].*)',fichier)
            langue = m.group(1)
            # Parcours du lexique phonétisé
            for line in lexPho:
                mot,phono = line.split("\t")
                print ("le mot "+mot+" se prononce "+phono)
                for i in range(0,len(phono)-1):
                    # On traite l'élément courant
                    # Cas des voyelles nasales en deux caractères API
                    if (phono[i] == "ɔ" or phono[i] == "ɑ" 
                        or phono[i] == "ɛ") and (phono[i+1] == "̃"):
                        courant = phono[i] + phono[i+1]
                        i += 1
                    # Cas normal
                    elif phono[i] != "̃":
                        courant = phono[i]
                    # On traite ensuite l'élément suivant
                    # Cas des voyelles nasales (2 caractères API)
                    if (phono[i+1] == "ɔ" or phono[i+1] == "ɑ" 
                        or phono[i+1] == "ɛ") and (phono[i+2] == "̃"):
                        suivant = phono[i+1] + phono[i+2]
                        i += 1
                    # Cas normal : on vérifie qu'il y a bien un élément suivant
                    elif phono[i+1] != "\n":
                        suivant = phono[i+1]
                    # On forme les paires
                    paire = courant+suivant
                    phoneme = courant
                    # Ajout de la paire au dictionnaire
                    # Si la paire ne figure pas encore dans le dictionnaire
                    if (paire not in dicoPaires.keys()):
                        # Ajout de la paire dans en clé + fréquence=1
                        dicoPaires[paire] = 1
                    else:
                        # Incrémentation de la fréquence
                        dicoPaires[paire] += 1
                    if courant not in listeP:
                        listeP.append(courant)
            lexPho.close()
        except IOError as e:
            print ("err n "+str(e.errno)+" lors de la lecture")
        # On stocke la liste des phonèmes dans un fichier spécifique
        try:
            # Création du fichier contenant tous les phonèmes
            outputName = repOut + "\\" + langue + "_phonemes.txt"
            ficPhonemes = open(outputName,mode="w",encoding="utf8")
            for phoneme in listeP:
                ficPhonemes.write(phoneme+"\n")
        except IOError as e:
            print ("err n "+str(e.errno)+" lors de l'écriture")
    del(listeP[:])
    try:
        # Création du fichier d'écriture du fichier de sortie
        monFichier = open("pairesAdj.txt","w",encoding="utf8")
        # Tri du dictionnaire contenant toutes les paires par value (fréquence)
        # (reverse pour tri décroissant)
        dicoPairesO = OrderedDict(sorted(dicoPaires.items(),
            key=lambda t:t[1],reverse=True))
        for key,value in dicoPairesO.items():
            monFichier.write("{0}\t{1}\n".format(key,value))
            # ~ print ("paire {0} (fréquence : {1})".format(key, value))
        monFichier.close()
    except IOError as e:
        print ("err n "+str(e.errno)
            +" lors de l'écriture des fichiers de paires")

rep = os.getcwd()
repIn = rep + "\\lexiques"
print(repIn)
repOut = rep + "\\phonemes"
print(repOut)
extractPaires(repIn,repOut)


