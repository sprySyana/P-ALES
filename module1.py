# coding: utf-8
# Python 3
# Projet P-ALES
# M2 IdL 2017-2018
# Anays Micolod & Célia Marion

import os
import re
from collections import OrderedDict


def extractPairs(folderLexicon,folderPhonemes,folderMain):
    """Extract pairs of phonemes and their frequencies for each phonetic lexicon."""
    print ("Extraction  des paires de phonèmes adjacents.")
    # Dictionnaire qui stocke chaque paire de phonèmes et ses fréquences
    dicPairs = {}
    # Liste qui stocke les phonèmes rencontrés pour chaque langue
    listP = []
    # Compteur du nombre de paires recensées
    # ~ nb_occ = 0
    # Création du dossier de sortie s'il n'existe pas
    if not os.path.isdir(folderPhonemes):
        os.mkdir(folderPhonemes)
    try:
        # On obtient la liste des fichiers du répertoire
        files = os.listdir(folderLexicon)
    except OSError as e:
        ("err n°{} lors de la lecture du dossier".format(e.errno))
        return False
    
    # On ouvre les lexiques un à un
    for f in files:
        try:
            lexPho = open(folderLexicon+"\\"+f,"r",encoding="utf8")
            # On récupère la langue dans le nom des fichiers
            m = re.search(r"(.*)([_].*)",f)
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
            outputName = os.path.join(folderPhonemes,language) + "_phonemes.txt"
            filePhonemes = open(outputName,mode="w",encoding="utf8") 
            for phoneme in listP: 
                filePhonemes.write(phoneme+"\n")
            filePhonemes.close()
        except IOError as e: 
            print ("err n°{} lors de l'écriture".format(e.errno))
        del(listP[:])
    try:
        # Création du fichier d'écriture de sortie
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
    print ("Vous pouvez retrouver le fichier de paires de phonèmes et de leurs fréquences dans le dossier :",folderMain,"\n")

