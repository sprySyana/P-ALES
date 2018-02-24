# coding: utf-8 

import os
import argparse

folderMain = os.getcwd() 
print("Chemin d'accès à votre dossier de travail :")
print("Path of working folder :")
print(folderMain,"\n")

folderLexicon = os.path.join(folderMain,"lexicons") 
print("Chemin attendu pour le dossier 'lexicons' :")
print("Expected path for 'lexicons' folder :")
print(folderLexicon,"\n") 

folderPhonemes = os.path.join(folderMain,"phonemes")
print("Chemin pour le dossier 'phonemes' qui est généré automatiquement :")
print("Path for the auto-generated folder 'phonemes' :")
print(folderPhonemes,"\n") 

folderSVG = os.path.join(folderMain,"svg")
print("Chemin attendu pour le dossier 'svg' :")
print("Expected path for 'svg' folder :")
print(folderSVG,"\n")

folderTemplate = os.path.join(folderSVG,"svg_template")
print("Chemin attendu pour le dossier 'SVG_template' :")
print("Expected path for 'SVG_template' folder :")
print(folderSVG,"\n")

folderInter = os.path.join(folderSVG,"svg_inter")
print("Chemin attendu pour le dossier 'SVG_inter' :")
print("Expected path for 'SVG_inter' folder :")
print(folderSVG,"\n")

folderFinaux = os.path.join(folderSVG,"svg_finaux")
print("Chemin attendu pour le dossier 'SVG_finaux' :")
print("Expected path for 'SVG_finaux' folder :")
print(folderSVG,"\n")

folderTest = os.path.join(folderSVG,"svg_test")
print("Chemin attendu pour le dossier 'SVG_test' :")
print("Expected path for 'SVG_test' folder :")
print(folderSVG,"\n")

folderClean = os.path.join(folderSVG,"svg_clean")
print("Chemin attendu pour le dossier 'SVG_clean' :")
print("Expected path for 'SVG_clean' folder :")
print(folderSVG,"\n")

folderInterface = os.path.join(folderMain,"interface")
print("Chemin attendu pour le dossier 'interface' :")
print("Expected path for 'interface' folder :")
print(folderSVG,"\n")
