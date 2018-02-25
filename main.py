# coding: utf-8
# python 3
# Projet P-ALES 
# M2 IdL 2017-2018 
# Anays Micolod & Célia Marion

import os
import config
from module1 import extractPairs
from module2 import construct_table
from module2 import construct_clean_table
from delta_color import setcolor_to_css


folderMain = config.folderMain
folderLexicon = config.folderLexicon 
folderPhonemes = config.folderPhonemes 
folderSVG = config.folderSVG
folderTemplate = config.folderTemplate
folderInter = config.folderInter
folderFinaux = config.folderFinaux
folderClean = config.folderClean
folderInterface = config.folderInterface

print ("---------------------------------------------------------------------------------------------------------------\n")
print ("\tBienvenue sur l'outil P-ALES\n")
print ("\tGénération d'une représentation chromatique des systèmes phonologiques")
print ("\tpour l'enseignement des langues sinogrammiques\n")
print ("\tCréé par Anays Micolod et Célia Marion\n")
print ("\tProjet professionnel - M2 IdL")
print ("\tUniversité Grenoble-Alpes\n")
print ("---------------------------------------------------------------------------------------------------------------\n")

# Variable contrôlant le choix fait par l'utilisateur
res_menu=0

while res_menu != 10:
    print ("\nVeuillez taper le numéro correspondant à l'option souhaitée et appuyer sur la touche \"entrée\" :\n")
    print ("\t 1 - Extraction des paires de phonèmes adjacents\n")
    print ("\t 2 - Calcul des nouvelles couleurs\n")
    print ("\t 3 - Ecriture du fichier CSS avec les nouvelles couleurs\n")
    print ("\t 4 - Production des tableaux\n")
    # ~ print("\t\t - Construction des tableaux intermédiaires")
    # ~ print("\t\t - Construction des tableaux finaux")
    
    res_menu = int(input("? - "))
    
    if res_menu == 1:
        # Lancement du script d'extraction des paires de phonèmes
        extractPairs(folderLexicon,folderPhonemes,folderMain)
    
    elif res_menu == 2:
        print ("Fonctionnalité non disponible sur l'interface pour le moment.\n")
    
    elif res_menu == 3:
        # Lancement du script d'écriture du nouveau CSS
        setcolor_to_css(folderMain,folderInterface)
    
    elif res_menu == 4:
        # Appel des fonctions du module2
        construct_table(folderMain,folderPhonemes,folderTemplate,folderInter)
        construct_clean_table(folderInter,folderClean)
    

