# *-* coding:utf-8 *-* 

import os
import argparse

rep = os.getcwd() 
print("Chemin d'acces à votre dossier de travail :")
print("Path of working folder :")
print(rep,"\n")

repIn = os.path.join(rep, "lexiques") 
print("Chemin attendu pour le dossier 'lexiques' :")
print("Expected path for 'lexiques' folder :")
print(repIn,"\n") 

repOut = os.path.join(rep, "phonemes")
print("Chemin pour le dossier 'phonemes' qui est généré automatiquement :")
print("Path for the auto-generated folder 'phonemes' :")
print(repOut,"\n") 
