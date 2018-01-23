# *-* coding:utf-8 *-* 
# Python 3

import os 
import re 
import config 
import argparse 
from collections import OrderedDict 

# Projet P-ALES 
# M2 IdL 2017-2018 
# Anays Micolod & Célia Marion 

# Il manque encore le cas des affriquées 

def extractPairs(repIn,repOut): 
    """ 
    fonction qui extrait les paires de phonèmes et leurs fréquences  
        pour chaque lexique phonétisé 
    repIn : string - le répertoire contenant les lexiques phonétisés 
    repOut : string - le répertoire contenant les fichiers de phonèmes 
    """ 
    # Instanciation des variables 
    dicoPairs = {} 
    listeP = [] 
    if not os.path.isdir(repOut): 
        os.mkdir(repOut) 
    try: 
        # On obtient la liste des fichiers du répertoire 
        files=os.listdir(repIn) 
    except OSError as e: 
        #~ ("err n "+str(e.errno)+" lors de la lecture du dossier") 
        ("err n°{} lors de la lecture du dossier".format(e.errno)) 
        return False 
    
    # On ouvre les lexiques un à un 
    for fichier in files: 
        try: 
            lexPho = open(os.path.join(repIn,fichier),"r",encoding="utf8") 
            # On récupère la langue dans le nom des fichiers 
            m = re.search(r'(.*)([_].*)',fichier) 
            langue = m.group(1) 
            # Parcours du lexique phonétisé 
            for line in lexPho: 
                word,phono = line.split("\t") 
                #~ print ("le mot "+mot+" se prononce "+phono) 
                print ("le mot {} se prononce {}".format(word,phono)) 
                for i in range(0,len(phono)-1): 
                    # On traite l'élément courant 
                    # Cas des voyelles nasales en deux caractères API 
                    if (phono[i] == "ɔ" or phono[i] == "ɑ"  
                        or phono[i] == "ɛ") and (phono[i+1] == "̃"): 
                        currentP = phono[i] + phono[i+1] 
                        i += 1 
                    # Cas normal 
                    elif phono[i] != "̃": 
                        currentP = phono[i] 
                    # On traite ensuite l'élément suivant 
                    # Cas des voyelles nasales (2 caractères API) 
                    if (phono[i+1] == "ɔ" or phono[i+1] == "ɑ"  
                        or phono[i+1] == "ɛ") and (phono[i+2] == "̃"): 
                        nextP = phono[i+1] + phono[i+2] 
                        i += 1 
                    # Cas normal : on vérifie qu'il y a bien un élément suivant 
                    elif phono[i+1] != "\n": 
                        nextP = phono[i+1] 
                    # On forme les paires 
                    pair = currentP+nextP 
                    phoneme = currentP 
                    # Ajout de la paire au dictionnaire 
                    # Si la paire ne figure pas encore dans le dictionnaire 
                    if (pair not in dicoPairs.keys()): 
                        # Ajout de la paire dans en clé + fréquence=1 
                        dicoPairs[pair] = 1 
                    else: 
                        # Incrémentation de la fréquence 
                        dicoPairs[pair] += 1 
                    if current not in listeP: 
                        listeP.append(current) 
            lexPho.close() 
        except IOError as e: 
            #~ print ("err n "+str(e.errno)+" lors de la lecture") 
            print ("err n°{} lors de la lecture".format(e.errno)) 
        # On stocke la liste des phonèmes dans un fichier spécifique 
        try: 
            # Création du fichier contenant tous les phonèmes 
            outputName = os.path.join(repOut,langue) + "_phonemes.txt" 
            filePhonemes = open(outputName,mode="w",encoding="utf8") 
            for phoneme in listeP: 
                filePhonemes.write(phoneme+"\n") 
        except IOError as e: 
            #~ print ("err n "+str(e.errno)+" lors de l'écriture") 
            print ("err n°{} lors de l'écriture".format(e.errno)) 
    del(listeP[:]) 
    try: 
        # Création du fichier d'écriture du fichier de sortie 
        myFile = open("pairesAdj.txt","w",encoding="utf8") 
        # Tri du dictionnaire contenant toutes les paires par value (fréquence) 
        # (reverse pour tri décroissant) 
        dicoPairsO = OrderedDict(sorted(dicoPairs.items(), 
            key=lambda t:t[1],reverse=True)) 
        for key,value in dicoPairsO.items(): 
            myFile.write("{0}\t{1}\n".format(key,value)) 
            # ~ print ("paire {0} (fréquence : {1})".format(key, value)) 
        myFile.close() 
    except IOError as e: 
         #~ print ("err n "+str(e.errno) lors de l'écriture des fichiers de paires") 
         print ("err n°{} lors de l'écriture du fichier de paires".format(e.errno))

# CLI

def helpParser():
    parser = argparse.ArgumentParser(description='extraction tableau [paire.: fréquence]') 
    parser.add_argument('--repIn', action='store_true',
                        help='chemin du dossier "lexiques"') 
    parser.add_argument('--repOut', action='store_true',
                        help='chemin du dossier "phonemes",'
                        +'ce dossier est généré par le programme s\'il n\'existe pas') 
    args = parser.parse_args() 
    
# recuperation des donées de config

repIn = config.repIn
repOut = config.repOut

# Appel des fonctions

helpParser()
print('les chemins sont modifiables dans "config.py"\n')

extractPairs(repIn,repOut) 
