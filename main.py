# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:27:39 2021

@author: Louis Lacoste & Emma Fernandez
"""
#------------------------------------------------------------------------------
#                       Imports nécessaires
#------------------------------------------------------------------------------
import sqlite3

#------------------------------------------------------------------------------
#                       Fonctions outils
#------------------------------------------------------------------------------

def tuple_vers_chaine(tuple):
    """
    Fonction qui transforme un tuple, e.g. ('CHEV. SAPIN 200x6x2', 75.0, 45), 
    en chaine de caractères en remplaçant la virgule avec une tabulation (\t)
    et renvoie cette chaine, e.g. 'CHEV. SAPIN 200x6x2'	 75.0	 45
    """
    chaine = str(tuple)     # le tuple est transformé en chaine
    chaine = chaine[1:-1]   # on enlève les parenthèses de début et de fin
    return (chaine.replace(",", "\t"))  # on remplace la virgule avec une tabulation
                                        # et on renvoie cette chaine
                                        
#------------------------------------------------------------------------------
#                  Fonctionnalités du vidéoclub
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#         Fonctions pour l'affichage de la liste des films
#------------------------------------------------------------------------------
def recuperer_infos_films():
    """ Fonction qui récupère les infos de chaque entrée de la table film """
    requeteSQL = """SELECT ID, TITRE, DATE_SORTIE, DUREE, GENRE, NATIONALITE 
    FROM film"""
    # Exécution de la requête
    curseur.execute(requeteSQL)

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_films") 

def recuperer_casting(id_film):
    requeteSQL = """SELECT acteur.PRENOM, acteur.NOM, role.LIBELLE
    FROM liste_acteurs, acteur, role
    WHERE liste_acteurs.ID_FILM = ?
    AND liste_acteurs.ID_ACTEUR = acteur.ID AND liste_acteurs.ID_ROLE = role.ID"""
    # Exécution de la requête
    curseur.execute(requeteSQL, [id_film])

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas d'entrée correspondante ! recuperer_casting ")     
    
def tuple_vers_casting(tuple):
    return "avec {} {} en tant que {}".format(tuple[0],tuple[1],tuple[2])

def unite_casting_vers_casting_lisible(liste_casting):
    chaine_casting = ""
    if len(liste_casting) == 1: # Si un seul acteur on retourne juste le str
        chaine_casting = liste_casting[0]
    else:
        j=0
        for i in range(len(liste_casting)):
            while j < len(liste_casting)-2: # Avant le dernier élément on met des virgules
                chaine_casting += liste_casting[j]+", "
                j+=1
        chaine_casting += liste_casting[-2] + " et " + liste_casting[-1]
    return chaine_casting


def afficher_films():
    print("Affichage des films")
    infos_films_tuples = recuperer_infos_films()
    infos_films = []
    for film in infos_films_tuples: # On convertit les tuples en liste pour manipuler les infos
        infos_films.append(list(film))
    for i in range(len(infos_films)):
        id_film = infos_films[i][0] # on recupere l'id du ieme film
        infos_casting = recuperer_casting(id_film)
        cast=[]
        for acteur_et_role in infos_casting:
            cast.append(tuple_vers_casting(acteur_et_role)) # On ajoute le cast dans la liste d'info
        infos_films[i].append(cast)
        print(infos_films[i])
    print("\nListe des films du vidéoclub : ")
    for film in infos_films:
        print("--")
        print("{} - {} ({}), {} min, {}, {}. Casting : {}".format(film[0],film[1],film[2],film[3],film[4],film[5], unite_casting_vers_casting_lisible(film[6])))

        

#------------------------------------------------------------------------------
#                  Fonctions pour la location
#------------------------------------------------------------------------------

def louer_film():
    print("Location d'un film")
    

#------------------------------------------------------------------------------
#               Fonctions pour vérifier les retours
#------------------------------------------------------------------------------

def verifier_retours():
    print("Vérification des retours")



#------------------------------------------------------------------------------
#                  Fonctions pour ajouter un film
#------------------------------------------------------------------------------

def ajouter_film():
    print("Ajout d'un film")

#------------------------------------------------------------------------------
#                  Fonctions pour retirer un film
#------------------------------------------------------------------------------


    
def retirer_film():
    print("Retrait d'un film")


#------------------------------------------------------------------------------
#                       Fonction de menu
#------------------------------------------------------------------------------

def menu():
    resterDansLeMenu = True
    while resterDansLeMenu:
        print("\n1 - Afficher la liste des films \n2 - Louer un film \n3 - Vérification des retours\n4 - Ajouter un film\n5 - Retirer un film \n--------\n0 pour quitter")
        choix = int(input("Veuillez sélectionner l'une des options ci-dessus (le numéro) : "))
        while choix not in [0,1,2,3,4,5]:
            print("Le choix doit se faire parmi les propositions ci-dessus !")
            print("\n1 - Afficher la liste des films \n2 - Louer un film \n3 - Vérification des retours\n4 - Ajouter un film\n5 - Retirer un film \n--------\n0 pour quitter")
            choix = int(input("Veuillez sélectionner l'une des options ci-dessus (le numéro) : "))
        if choix == 0:
            print("Au revoir !")
            return
        elif choix == 1:
            afficher_films()
        elif choix == 2:
            louer_film()
        elif choix == 3:
            verifier_retours()
        elif choix == 4:
            ajouter_film()
        elif choix == 5:
            retirer_film()
        else:
            print("Erreur de choix !")
        
#------------------------------------------------------------------------------
#                       Corps du programme
#------------------------------------------------------------------------------
# 1. connexion à la base de données
connexion = sqlite3.connect("film.sqlite")  	

# 2. création d'un curseur d'échange
curseur = connexion.cursor()   

# 3. exécution de requête et 4. traitement du résultat 
# dans un appel de la fonction:
menu()

# 5. Fermeture de la connexion
curseur.close()
connexion.close() #fermeture de la connexion à la base de données