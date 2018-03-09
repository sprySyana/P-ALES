# coding: utf-8
# python 3
# Projet P-ALES 
# M2 IdL 2017-2018 
# Anays Micolod & Célia Marion 

import os 
import re 
from math import sqrt
from lxml import etree


def construct_table(folderMain,folderPhonemes,folderTemplate,folderInter):
    """Construct SVG intermédiaire à partir d'un SVG patron."""
    print ("Construction des tableaux SVG intermédiaires.")
    # Récupérer les entrées
    #   Retrieve entry data
    filesPhonList = os.listdir(folderPhonemes)
    # Liste des phonèmes
    #   phonems list
    phonemesList = []
    # Dictionnaire associant le code Xsampa à la notation API de chaque phonème
    #   Creation of [Xsampa : IPA] dictionary
    codes_phonemes = {}
    
    # Création du dossier de sortie s'il n'existe pas
    #   Create folder if not existing/specified
    if not os.path.isdir(folderInter):
        os.mkdir(folderInter)
    
    # On récupère l'association code Xsampa - notation API que l'on met
    # dans le dictionnaire codes_phonemes
    #   Read the file to fill the [Xsampa : IPA] dic
    try:
        file_code = open("Xsampa-API.txt","r",encoding="utf8")
        content = file_code.read()
        lines_code = content.split("\n")
        for line in lines_code:
            col = line.split("\t")
            if len(col)>1:
                # Extraction de la correspondance code/api du CSS
                #   Extract connection btw IPA and modified Xsampa notation ("code")
                code = col[0]
                api = col[1]
                codes_phonemes[code] = api
        # ~ print ("codes_phonemes : ",codes_phonemes)
        file_code.close()
    except IOError as e: 
        print ("err n°{} lors de la lecture du fichier Xsampa-API".format(e.errno))
    
    # Parcours des fichiers contenant les listes de phonèmes
    #   Browse phonems files
    for filePh in filesPhonList:
        cpt = 0
        motif = re.search(r"(.*)([_].*)",filePh)
        language = motif.group(1)
        # ~ print ("\nlangue : ",language)
        # On ne produit pas de tableau pour le français et l'anglais
        #   Exclusion of French and English
        if (language != "french" and language != "english"):
            cpt_phonemes = 0
            try:
                # Ouverture du fichier de phonèmes
                #   Open phonems file
                file_phonemes = open(os.path.join(folderPhonemes,filePh),"r",encoding="utf8")
                content = file_phonemes.read()
                lines = content.split("\n")
                for line in lines:
                    phoneme = line.split("\n")
                    # On ajoute le phonème à la liste des phonèmes
                    #   Add phonem to phonem list
                    phonemesList += phoneme
                    cpt_phonemes += 1
                file_phonemes.close()
            except IOError as e:
                print ("err n°{} lors de la lecture du fichier de phonèmes".format(e.errno))
            # ~ print ("phonemesList : ",phonemesList)
            # ~ print (cpt_phonemes)
            
            # Ouverture du fichier SVG patron
            #   Open "blueprint" SVG file
            file_SVG = open(os.path.join(folderTemplate,"patron.svg"),"r",encoding="utf8")
            content = file_SVG.read()
            lines = content.split("\n")
            
            try:
                # Création du fichier SVG intermédiaire
                #   Create Intermediary SVG
                outputName = os.path.join(folderInter,language) + ".svg"
                file_inter = open(outputName,"w",encoding="utf8")
                sortir = False
                # Indice de parcours du fichier
                #   counter for line in file
                i = 0
                # Indice de parcours du début du fichier
                #   counter for lines treated
                debut = 0
                while (i < len(lines) and sortir == False):
                    # On répère dans le svg les codes de phonèmes
                    #   Spot phonem code in SVG's XML
                    m = re.search(r"id=\"g_(\w+)\"",lines[i])
                    if not m:
                        file_inter.write(lines[i]+"\n")
                        debut += 1
                        i += 1
                    else :
                        sortir = True
                # on met à jour le compteur pour reprendre
                #   setback counter
                i = debut
                while i < len(lines):
                    # On récupère le nom de la zone
                    #   Retrieve zone name ('type/category' of phonem)
                    m1 = re.search(r"id=\"g_(\w+)\"",lines[i])
                    if m1:
                        cpt += 1
                        zone = m1.group(1)
                        # ~ print ("n°",cpt,"\tzone :",zone)
                        # Pour la première zone, la balise <g est écrite
                        #   For 1st zone, the "<g" is already written
                        # par la boucle précédente
                        if cpt == 1:
                            file_inter.write("       id=\"g_"+zone+"\">\n")
                            i += 1
                        # Autrement, il faut fermer la dernière balise g
                        #   Else we have to close previous G and open new one
                        # et ouvrir la nouvelle
                        else:
                            file_inter.write("    </g>\n")
                            file_inter.write("    <g\n")
                            file_inter.write("       id=\"g_"+zone+"\">\n")
                            i += 1
                    # On récupère l'identifiant du rectangle : code du phonème
                    #   Retrieve rectangle Id = rect_(phonem code)
                    m = re.search(r"class=\"(\w+)\"",lines[i])
                    if m:
                        code_ph = m.group(1)
                        # ~ print ("code_ph :",code_ph)
                        # Traitement pour chaque phonème de la liste
                        #   Handling for each phonem in list
                        for ph in phonemesList:
                            # On récupère son code xsampa dans codes_phonemes
                            #   Get Xsampa code in codes_phonemes
                            for j in codes_phonemes:
                                # Si la notation API correspond au phonème :
                                #   If API matches to phonem
                                if codes_phonemes[j] == ph:
                                    # On crée un dictionnaire inversé pour pouvoir
                                    #   Create reverted dico
                                    # récupérer la clé de codes_phonemes
                                    #   To retrieve key in codes_phonemes
                                    d_inv = {v: k for k, v in codes_phonemes.items()}
                                    code_xsampa = d_inv[ph]
                                    # ~ print(code_xsampa,ph)
                                    if code_ph == code_xsampa:
                                        # ~ print ("code_ph : ",code_ph," code_xsampa : ",code_xsampa)
                                        file_inter.write("      <rect\n")
                                        file_inter.write("         class=\""+code_ph+"\"\n")
                                        file_inter.write(lines[i+1]+"\n")
                                        file_inter.write(lines[i+2]+"\n")
                                        file_inter.write(lines[i+3]+"\n")
                                        file_inter.write(lines[i+4]+"\n")
                                        file_inter.write(lines[i+5]+"\n")
                                        i += 5
                    i += 1
                # On écrit enfin les deux (trois) dernières lignes du SVG
                #   Add the last (2~3) lines of the SVG file
                file_inter.write("    </g>\n  </g>\n</svg>")
                # Fin du traitement = fermeture des fichiers
                #   Handling finished = closing file
                file_inter.close()
            except IOError as e: 
                print ("err n°{} lors de l'écriture du SVG intermédiaire".format(e.errno))
        # On remet la liste des phonèmes à 0 pour passer à la langue suivante
        #   Setback phonem list to 0 before treating new langue
        del(phonemesList[:])
    print ("Vous pouvez retrouver les tableaux SVG intermédiaires dans le dossier :",folderInter,"\n")

def construct_clean_table(folderInter,folderClean):
    """Same SVG but without line 9 so it is 'parsable'"""
    # Création du dossier de sortie s'il n'existe pas
    #   Create folder if not existing/not specified
    if not os.path.isdir(folderClean):
        os.mkdir(folderClean)
    filesInterList = os.listdir(folderInter)
    # Parcours des fichiers SVG un à un
    #   Skim SVG files one by one
    for fileInter in filesInterList:
        try:
            # Ouverture du fichier en écriture
            #   Open writting file
            file_inter = open(os.path.join(folderInter,fileInter),"r",encoding="utf8")
            m = re.search(r"(\w+)\.svg",fileInter)
            language = m.group(1)
            content = file_inter.read()
            lines = content.split("\n")
            try:
                # Création du fichier SVG intermédiaire Clean
                #   Create Clean Intermediary SVG file
                outputName = os.path.join(folderClean,language) + "_clean.svg"
                file_clean = open(outputName,"w",encoding="utf8")
                i = 0
                debut = 0
                # On écrit les 8 premières lignes
                #   Write 8 first lines
                while i < 8:
                    file_clean.write(lines[i]+"\n")
                    debut += 1
                    i +=1
                i = debut+1
                # On écrit les lignes suivantes à partir de la 10ème
                #   Write other lines starting from 10th
                while i < len(lines):
                    file_clean.write(lines[i]+"\n")
                    i += 1
                file_clean.close()
            except OSError as e:
                print ("err n°{} lors de l'écriture du fichier".format(e.errno))
            file_inter.close()
        except OSError as e:
            print ("err n°{} lors de la lecture du fichier".format(e.errno))
    print ("Vous pouvez retrouver les tableaux SVG intermédiaires \"clean\" dans le dossier :",folderClean,"\n")

