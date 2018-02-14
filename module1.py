# coding: utf-8
# Python 3

import os
import re
import config 
import argparse
from collections import OrderedDict

# Projet P-ALES
# M2 IdL 2017-2018
# Anays Micolod & Célia Marion


def extractPairs(repIn,repOut):
    """
    fonction qui extrait les paires de phonèmes et leurs fréquences 
        pour chaque lexique phonétisé
    repIn : string - le répertoire contenant les lexiques phonétisés
    repOut : string - le répertoire contenant les fichiers de phonèmes
    """
    # Instanciation des variables
    dicPairs = {}
    listP = []
    if not os.path.isdir(repOut):
        os.mkdir(repOut)
    
    try:
        # On obtient la liste des fichiers du répertoire
        files = os.listdir(repIn)
    except OSError as e:
        ("err n°{} lors de la lecture du dossier".format(e.errno))
        return False
    
    # On ouvre les lexiques un à un
    for f in files:
        try:
            lexPho = open(repIn+"\\"+f,"r",encoding="utf8")
            # On récupère la langue dans le nom des fichiers
            m = re.search(r'(.*)([_].*)',f)
            language = m.group(1)
            # Parcours du lexique phonétisé
            for line in lexPho:
                phono = line.split(" ")
                # ~ print (phono)
                for i in range(0,len(phono)-2):
                    if (phono[i] != "\n"):
                        # élément courant : current
                        courant = phono[i]
                        # élément suivant : next
                        suivant = phono[i+1]
                        # On forme les paires
                        # ~ print ("paire : "+courant+" et "+suivant)
                        paire = courant+"\t"+suivant
                        phoneme = courant
                        # Ajout de la paire au dictionnaire
                        # Si la paire ne figure pas encore dans le dictionnaire
                        if (paire not in dicPairs.keys()):
                            # Ajout de la paire dans en clé + fréquence=1
                            dicPairs[paire] = 1
                        else:
                            # Incrémentation de la fréquence
                            dicPairs[paire] += 1
                        if courant not in listP:
                            listP.append(courant)
            lexPho.close()
        except IOError as e:
            print ("err n°{} lors de la lecture".format(e.errno))
        # On stocke la liste des phonèmes dans un fichier spécifique
        try: 
            # Création du fichier contenant tous les phonèmes 
            outputName = os.path.join(repOut,language) + "_phonemes.txt" 
            filePhonemes = open(outputName,mode="w",encoding="utf8") 
            for phoneme in listP: 
                filePhonemes.write(phoneme+"\n") 
        except IOError as e: 
            print ("err n°{} lors de l'écriture".format(e.errno))
        del(listP[:])
    try:
        # Création du fichier d'écriture du fichier de sortie
        filePairs = open("pairesAdj.txt","w",encoding="utf8")
        # Tri du dictionnaire contenant toutes les paires par value (fréquence)
        # (reverse pour tri décroissant)
        dicPairsO = OrderedDict(sorted(dicPairs.items(),
            key=lambda t:t[1],reverse=True))
        for key,value in dicPairsO.items():
            filePairs.write("{0}\t{1}\n".format(key,value))
        filePairs.close()
    except IOError as e:
        print ("err n°{} lors de l'écriture du fichier de paires".format(e.errno))

# CLI
def helpParser():
    parser = argparse.ArgumentParser(description = "extraction tableau [paire.: fréquence]")
    parser.add_argument("--repIn", action="store_true",
                        help="chemin du dossier \"lexiques\"") 
    parser.add_argument("--repOut", action = "store_true",
                        help="chemin du dossier \"phonemes\","
                        + "ce dossier est généré par le programme s'il n'existe pas")
    args = parser.parse_args() 
    
# récupération des données de config
repIn = config.repIn
repOut = config.repOut

# Appel des fonctions
helpParser()
print("les chemins sont modifiables dans \"config.py\"\n")

extractPairs(repIn,repOut)


