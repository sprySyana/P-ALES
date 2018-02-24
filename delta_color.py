# coding: utf-8

import re
import os
import webcolors


# Fonction permettant facilement de passer du format hexadécimal aux valeurs R,G,B d'une couleur
def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def setcolor_to_css(folderMain,folderInterface):
    """Re-write CSS file for the given set of colors."""
    # Liste qui stocke les phonèmes et couleurs associées
    list_colors = []
    # Booléen 
    trouve = False
    
    try:
        # Ouverture du fichier contenant le set de couleurs
        file_color = open("new_set_colors.txt",mode="r",encoding="utf8")
        content = file_color.read()
        lines = content.split("\n")
        # Lecture ligne par ligne
        for line in lines:
            col = line.split("\t")
            if len(col)>1:
                # On récupère les phonèmes et les couleurs
                ph_api = col[0]
                color = col[1]
                # On ajoute un tuple formé des 2 phonèmes à la liste des paires
                list_colors.append((ph_api,color))
        file_color.close()
    except IOError as e:
        print ("err n°{} lors de la lecture du fichier contenant le set de couleurs".format(e.errno))
    # ~ print ("list_colors :",list_colors)
    
    try:
        file_style_w = open(os.path.join(folderInterface+"\\test_style.css"),mode="w",encoding="utf8")
        try:
            # Ouverture fichier CSS
            file_style = open(os.path.join(folderInterface+"\\style.css"),mode="r",encoding="utf8")
            content = file_style.read()
            lines = content.split("\n")
            i = 0
            # Lecture ligne par ligne
            while i < len(lines)-1:
                # On cherhce le pattern
                m = re.search(r"\.(\w+)\t{fill:(.*)}\t/\* (.*?) ",lines[i])
                if m:
                    ph_xsampa = m.group(1)
                    hex_color = m.group(2)
                    ph_api = m.group(3)
                    # parcours de list_colors
                    for ph in list_colors:
                        phoneme = ph[0]
                        color = ph[1]
                        if phoneme == ph_api:
                            trouve = True
                            break
                        else:
                            trouve = False
                    if trouve == True:
                        replace = re.sub(hex_color,color,lines[i])
                        # ~ print (replace+"\n")
                        file_style_w.write(replace+"\n")
                    else:
                        # ~ print (lines[i]+"\n")
                        file_style_w.write(lines[i]+"\n")
                # Pour écrire les première lignes
                else:
                    file_style_w.write(lines[i]+"\n")
                i += 1
                
            file_style.close()
        except IOError as e:
            print ("err n°{} lors de la lecture du fichier style.css".format(e.errno))
        
        file_style_w.close()
    except IOError as e:
            print ("err n°{} lors de l'écriture du fichier test_style.css".format(e.errno))
    print (os.path.realpath(os.path.join(folderInterface,"style.css")))
    print (os.path.realpath(os.path.join(folderInterface,"test_style.css")))
    # On supprime l'ancien fichier CSS
    os.remove(os.path.realpath(os.path.join(folderInterface,"style.css")))
    # On renomme les nouveau fichier CSS pour qu'il soit utilisé
    os.rename(os.path.realpath(os.path.join(folderInterface,"test_style.css")),os.path.realpath(os.path.join(folderInterface,"style.css")))
    print ("Vous pouvez retrouver le CSS modifié en fonction des nouvelles couleurs calculées dans le dossier :",folderInterface,"\n")



