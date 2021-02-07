# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 17:27:39 2021

@author: Louis Lacoste & Emma Fernandez
"""
#------------------------------------------------------------------------------
#                       Imports nécessaires
#------------------------------------------------------------------------------
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta

#------------------------------------------------------------------------------
#                    Définition des constantes
#------------------------------------------------------------------------------
verifier_les_retours_aujourdhui = False

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
            # Avant le dernier élément on met des virgules
            while j < len(liste_casting)-2: 
                chaine_casting += liste_casting[j]+", "
                j+=1
        chaine_casting += liste_casting[-2] + " et " + liste_casting[-1]
    return chaine_casting


def afficher_films():
    print("\n--------\nAffichage des films")
    infos_films_tuples = recuperer_infos_films()
    infos_films = []
    for film in infos_films_tuples: 
    # On convertit les tuples en liste pour manipuler les infos
        infos_films.append(list(film))
    for i in range(len(infos_films)):
        id_film = infos_films[i][0] # on recupere l'id du ieme film
        infos_casting = recuperer_casting(id_film)
        cast=[]
        for acteur_et_role in infos_casting:
            # On ajoute le cast dans la liste d'info
            cast.append(tuple_vers_casting(acteur_et_role)) 
        infos_films[i].append(cast)
    print("\nListe des films du vidéoclub : ")
    for film in infos_films:
        print("--")
        print("{} - {} ({}), {} min, {}, {}. Casting : {}".format(film[0],
                                                                  film[1],
                                                                  film[2],
                                                                  film[3],
                                                                  film[4],
                                                                  film[5], 
                               unite_casting_vers_casting_lisible(film[6])))
    print("\n--------\n")

        

#------------------------------------------------------------------------------
#                  Fonctions pour la location
#------------------------------------------------------------------------------

def recuperer_infos_film_par_id(id_film):
    """ Fonction qui récupère les infos d'une entrée de la table film """
    requeteSQL = """SELECT ID, TITRE, DATE_SORTIE, DUREE, GENRE, NATIONALITE 
    FROM film WHERE id = ?"""
    # Exécution de la requête
    curseur.execute(requeteSQL, [id_film])

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return list(resultat[0])
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_film_par_id")

def recuperer_supports_par_id_film(id_film):
    requeteSQL = """SELECT id, type_support, prix, quantite
    FROM support
    WHERE ? = id_film"""
    curseur.execute(requeteSQL, [id_film])
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas de support dispo !")
        return 0
        
def compter_nombre_fois_supports_loues(id_support):
    """
    Parameters
    ----------
    id_support : int
        L'id du support dans la table support.

    Returns
    -------
    int
        Renvoie le nombre de fois que ce support a été loué.
    """
    requeteSQL = """SELECT COUNT(distinct id)
    FROM location
    WHERE id_support = ?
    """
    curseur.execute(requeteSQL, [id_support])
    resultat = curseur.fetchall() 
    nbre_de_fois_loues = resultat[0][0]
    return nbre_de_fois_loues

def afficher_supports_disponibles_par_id_film(id_film):
    tuple_de_supports = recuperer_supports_par_id_film(id_film)
    # On gère le cas où il n'existe pas de support pour ce film
    if tuple_de_supports == 0:
        return 0
    liste_de_supports = []
    for i in range(len(tuple_de_supports)):
        liste_de_supports.append([i]+list(tuple_de_supports[i]))
    print("\nSupports disponibles :")
    for support in liste_de_supports:
        quantite_disponible  = support[4] - compter_nombre_fois_supports_loues(support[1])
        if quantite_disponible > 0:
            print("--------")
            print("{} - {}, prix de location : {} euros, quantité disponible : {}".format(
                support[0]+1,
                support[2],
                support[3],
                quantite_disponible))
        else:
            print("{}, prix de location : {} euros, pas en stock pour l'instant".format(
                support[2],
                support[3]))
            print("--------")
    return liste_de_supports

def date_plus_1_mois(date):
    plus_un_mois = relativedelta(months=1)
    nouvelle_date = date + plus_un_mois
    return nouvelle_date
        
def insertion_location(email, id_support, date_debut, date_fin):
    requeteSQL = """INSERT INTO location(email, id_support, date_debut, date_fin)
    VALUES (?, ?, ?, ?)"""
    curseur.execute(requeteSQL, [email, id_support, date_debut, date_fin])    
    connexion.commit()


def louer_film():
    print("\n--------\nLocation d'un film pour 1 mois : ")
    liste_id_films_disponibles = [0]
    for film in recuperer_infos_films():
        # On récupère les indices des films existants
        liste_id_films_disponibles.append(film[0])
    afficher_films()
    print("--------\n0 pour quitter")
    choix = int(input("""Veuillez sélectionner
l'une des options ci-dessus (le numéro du film) : """))
    while choix not in liste_id_films_disponibles:
        afficher_films()
        print("--------\n0 pour quitter")
        print("Le choix doit se faire parmi les propositions ci-dessus !")
        choix = int(input("""Veuillez sélectionner l'une 
des options ci-dessus (le numéro du film) : """))
    if choix == 0: # Si on choisit 0 on quitte la fonction
        print("Location annulée !")
        return
    id_film = choix
    infos_film = recuperer_infos_film_par_id(id_film)
    print("\nFilm sélectionné :")
    print("{} - {} ({}), {} min, {}, {}.".format(infos_film[0],
                                                 infos_film[1],
                                                 infos_film[2],
                                                 infos_film[3],
                                                 infos_film[4],
                                                 infos_film[5]))
    liste_de_supports = afficher_supports_disponibles_par_id_film(id_film)
    if liste_de_supports == 0:
        print("Impossible louer ce film, il n'y a pas de supports du tout")
        return
    print("--------\n0 pour quitter")
    # On initialise avec -1 qui code pour quitter
    liste_id_selection_supports_disponibles = [-1]
    for support in liste_de_supports:
        liste_id_selection_supports_disponibles.append(support[0])
    choix_de_support = int(input("""Veuillez sélectionner
l'une des options ci-dessus (le numéro du support) : """))-1
    while choix_de_support not in liste_id_selection_supports_disponibles:
        # On vérifie que l'on choisit parmi 
        # les ids de selection (pas les id de supports !!!)
        print("\nFilm sélectionné :")
        print("{} - {} ({}), {} min, {}, {}.".format(infos_film[0],
                                                 infos_film[1],
                                                 infos_film[2],
                                                 infos_film[3],
                                                 infos_film[4],
                                                 infos_film[5]))
        liste_de_supports = afficher_supports_disponibles_par_id_film(id_film)
        print("--------\n0 pour quitter")
        print("Le choix doit se faire parmi les propositions ci-dessus !")
        choix_de_support = int(input("""Veuillez sélectionner
l'une des options ci-dessus (le numéro du support) : """))-1
    if choix_de_support == -1:
        print("Location annulée !")
        return # On termine la fonction
    id_selection_support = choix_de_support # On enregistre l'id sélectionné
    date_debut = date.today()
    date_fin = date_plus_1_mois(date_debut)
    support_choisi = liste_de_supports[id_selection_support]
    id_support = support_choisi[1]
    
    print("--------\nRécapitulatif :")
    # Durée de location
    print("Location du {} au {} ".format(date_debut, date_fin))
    print("Type de support : {} au prix de {} euros pour la location".format(
        support_choisi[2],
        support_choisi[3]))
    print("--------")
    email = input("Veuillez saisir l'email (sous la forme : johndoe@awebsite.com) : ")
    valider_email = input("L'email : {} est bien saisi ? (saisir o ou n pour oui ou non) : ".format(email))
    while valider_email == "" or valider_email.lower()[0] != "o":
        email = input("Veuillez saisir l'email (sous la forme : johndoe@awebsite.com): ")
        valider_email = input("L'email : {} est bien saisi ? (saisir o ou n pour oui ou non) : ".format(email))
    insertion_location(email, id_support, date_debut, date_fin)
    print("Location enregistrée !\n--------\n")
    
    
#------------------------------------------------------------------------------
#               Fonctions pour afficher les locations
#------------------------------------------------------------------------------

def recuperer_id_locations():
    requeteSQL = """SELECT id FROM location"""
    # Exécution de la requête
    curseur.execute(requeteSQL)

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        liste_id_locations = []
        for location in resultat:
            liste_id_locations.append(location[0])
        return liste_id_locations
    else:
        print("Pas d'entrée correspondante ! recuperer_id_locations")

def recuperer_infos_location(id_location):
    requeteSQL = """SELECT film.titre,  support.type_support, 
    email, date_debut, date_fin, support.prix 
    FROM location, film, support
    WHERE location.id = ?
    AND id_support = support.id
    AND support.id_film = film.id"""
    # Exécution de la requête
    curseur.execute(requeteSQL, [id_location])

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat[0]
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_location")

def afficher_locations():
    print("Liste des locations : \n--------")
    liste_id_locations = recuperer_id_locations()
    for id_location in liste_id_locations:
        location = recuperer_infos_location(id_location)
        print("ID : {} - {} en {} par {} du {} au {} pour {} euros\n".format(
            id_location,
            location[0],
            location[1],
            location[2],
            location[3],
            location[4],
            location[5]))
    print("--------")


#------------------------------------------------------------------------------
#               Fonctions pour vérifier les retours
#------------------------------------------------------------------------------

def recupere_locations_finies_aujourdhui():
    requeteSQL = """SELECT id, email, id_support, date_debut, date_fin
    FROM location
    WHERE date_fin <= CURRENT_DATE"""
    curseur.execute(requeteSQL)
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas de locations qui finissent ce jour")
    
def retour_en_stock(id_support):
    requeteSQL = """UPDATE support
    SET quantite = quantite + 1
    WHERE id = ?"""
    curseur.execute(requeteSQL, [id_support])
    connexion.commit()

def supprimer_location(id_location):
    requeteSQL = """DELETE FROM location
    WHERE id = ?"""
    curseur.execute(requeteSQL, [id_location])
    connexion.commit()
    
def verifier_retours():
    print("Vérification des retours")
    liste_locations_finies = recupere_locations_finies_aujourdhui()
    nombre_locations_revenues = 0
    for location_finie in liste_locations_finies:
        # On récupère l'id de la location échue
        id_location = location_finie[0]
        # On récupère les infos de la location échue
        infos_location_finie=recuperer_infos_location(id_location)
        print("Pour la location :\nID : {} - {} en {} par {} du {} au {} pour {} euros\n".format(
            id_location,
            infos_location_finie[0],
            infos_location_finie[1],
            infos_location_finie[2],
            infos_location_finie[3],
            infos_location_finie[4],
            infos_location_finie[5]))
        valider_suppression_location = input("Le support est revenu en stock ? (saisir o ou n pour oui ou non) : ")
        while valider_suppression_location == "" or valider_suppression_location.lower()[0] != "o" or valider_suppression_location.lower()[0] != "n":
            valider_suppression_location = input("Le support est revenu en stock ? (saisir o ou n pour oui ou non) : ")
        if valider_suppression_location.lower()[0] == "o":
            supprimer_location(id_location)
            nombre_locations_revenues += 1
        elif valider_suppression_location.lower()[0] == "n":
            print("La location n'est pas revenue, penser à renvoyer un mail à {}".format(infos_location_finie[2]))
    return

#------------------------------------------------------------------------------
#                  Fonctions pour ajouter un film
#------------------------------------------------------------------------------

def saisir_infos_film():
    validation = False
    while not validation:
        print("--------\nSaisie des informations du film :\n")
        titre = input("Veuillez saisir le titre : ")
        date_sortie = input("Veuillez saisir le date de sortie (annnée-mois-jour) : ")
        duree = int(input("Veuillez saisir la durée (en minutes, juste le nombre entier, sans min ou h) : "))
        genre = input("Veuillez saisir le genre : ").capitalize()
        nationalite = input("Veuillez saisir la nationalité : ").upper()
        print("Récapitulatif : {} ({}), {} min, {}, {}.\n--------".format(
        titre,
        date_sortie,
        duree,
        genre,
        nationalite))
        valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        while valider_saisie.lower()[0] not in ["o","n","q"]:
            print("Veuillez répondre par oui ou non.")
            valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        if valider_saisie.lower()[0] == "q":
            print("Ajout annulé !\n--------")
            return "q"
        elif valider_saisie.lower()[0] == "o":
            validation = True
            return (titre, date_sortie, duree, genre, nationalite)
        elif valider_saisie.lower()[0] == "n":
            validation = False


def inserer_film(titre, date_sortie, duree, genre, nationalite):
    requeteSQL = """INSERT INTO film (titre, date_sortie, duree, genre, nationalite)
    VALUES (?, ?, ?, ?, ?)"""
    curseur.execute(requeteSQL, [titre, date_sortie, duree, genre, nationalite])    
    connexion.commit()
    
def recuperer_id_film(titre, date_sortie, duree, genre, nationalite):
    requeteSQL = """SELECT id
    FROM film
    WHERE titre = ?
    AND date_sortie = ?
    AND duree = ?
    AND genre = ?
    AND nationalite = ?"""
    curseur.execute(requeteSQL, [titre, date_sortie, duree, genre, nationalite])
    resultat = curseur.fetchall()
    if resultat:
        return resultat[0][0]
    else:
        print("Pas d'entrée correspondante ! recuperer_id_film")
        
# Gestion des acteurs

def inserer_acteur(nom, prenom, site_web):
    requeteSQL="""INSERT INTO acteur(nom,prenom,site_web) VALUES (?, ?, ?)"""
    curseur.execute(requeteSQL, [nom, prenom, site_web])    
    connexion.commit()

def ajouter_acteur():
    validation = False
    while not validation:
        print("--------\nSaisie des informations de l'acteur :\n")
        nom = input("Veuillez saisir le nom : ").capitalize()
        prenom = input("Veuillez saisir le prénom : ").capitalize()
        site_web = input("Veuillez saisir le site web (facultatif, Entrée pour passer) : ")
        if site_web == "":
            print("{} {}".format(prenom, nom))
        elif site_web != "":
            print("{} {} ({})".format(prenom, nom, site_web))
        valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        while valider_saisie.lower()[0] not in ["o","n","q"]:
            print("Veuillez répondre par oui ou non.")
            valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        if valider_saisie.lower()[0] == "q":
            print("Ajout annulé !\n--------")
            return "q"
        elif valider_saisie.lower()[0] == "o":
            validation = True
            return (nom, prenom, site_web)
        elif valider_saisie.lower()[0] == "n":
            validation = False
            
def nouveaux_acteurs():
    print("\n--------\nAjout de nouveaux acteurs")
    afficher_acteurs()
    termine = False
    while not termine:
        infos_acteur = ajouter_acteur()
        if infos_acteur == "q":
        # Si on veut quitter
            return
        nom, prenom, site_web = infos_acteur
        inserer_acteur(nom, prenom, site_web)
        print("{} {} ajouté !".format(nom, prenom))
        continuer = input("Voulez-vous continuer à ajouter de nouveaux acteurs ? (o pour oui ou n pour non) : ")
        while continuer.lower()[0] not in ["o","n"]:
            print("Saisie incorrecte !")
            continuer = input("Voulez-vous continuer à ajouter de nouveaux acteurs ? (o pour oui ou n pour non) : ")
        if continuer.lower()[0] == "n":
            termine = True
    
def recuperer_infos_acteurs():
    """ Fonction qui récupère les infos de chaque entrée de la table acteur """
    requeteSQL = """SELECT ID, NOM, PRENOM, SITE_WEB 
    FROM acteur"""
    # Exécution de la requête
    curseur.execute(requeteSQL)

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_acteurs")

def afficher_acteurs():
    infos_acteurs = recuperer_infos_acteurs()
    liste_ids_acteurs = []
    print("\n--------\nAffichage des acteurs\n")
    for acteur in infos_acteurs:
        liste_ids_acteurs.append(acteur[0])
        if acteur[3] != "":
            print("{} - {} {} ({})".format(acteur[0], 
                                      acteur[2], 
                                      acteur[1], 
                                      acteur[3]))
        else:
            print("{} - {} {}".format(acteur[0],
                                      acteur[2],
                                      acteur[1]))
    print("--------\n")
    return liste_ids_acteurs

def recuperer_infos_acteurs_par_id(id_acteur):
    """ Fonction qui récupère les infos d'une entrée de la table acteur pour un id_acteur"""
    requeteSQL = """SELECT NOM, PRENOM, SITE_WEB 
    FROM acteur
    WHERE id = ?"""
    # Exécution de la requête
    curseur.execute(requeteSQL, [id_acteur])

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        if resultat[0][2] != "":
            # Résultat sous la forme Prénom Nom (Site Web)
            return "{} {} ({})".format(resultat[0][1], resultat[0][0], resultat[0][2])
        elif resultat[0][2] == "":
            # Résultat sous la forme Prénom Nom
            return "{} {}".format(resultat[0][1], resultat[0][0])
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_acteurs")    

# Gestion des roles

def inserer_role(libelle_role):
    requeteSQL="""INSERT INTO role(libelle) VALUES (?)"""
    curseur.execute(requeteSQL, [libelle_role])    
    connexion.commit()

def ajouter_role():
    validation = False
    while not validation:
        print("--------\nSaisie des informations du rôle :\n")
        libelle_role = input("Veuillez saisir le libelle du rôle : ")
        valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        while valider_saisie.lower()[0] not in ["o","n", "q"]:
            print("Veuillez répondre par oui ou non.")
            valider_saisie = input("Ces informations sont-elles correctes ? (o pour oui, n pour non ou q pour quitter) : ")
        if valider_saisie.lower()[0] == "q":
            print("Ajout annulé !\n--------")
            return "q"
        elif valider_saisie.lower()[0] == "o":
            validation = True
            return libelle_role
        elif valider_saisie.lower()[0] == "n":
            validation = False
            
def nouveaux_roles():
    print("\n--------\nAjout de nouveaux roles")
    afficher_roles()
    termine = False
    while not termine:
        infos_role = ajouter_role()
        if infos_role == "q":
        # Si on veut quitter
            return
        libelle_role = infos_role
        inserer_role(libelle_role)
        print("{} ajouté !".format(infos_role))
        continuer = input("Voulez-vous continuer à ajouter de nouveaux roles ? (o pour oui ou n pour non) : ")
        while continuer.lower()[0] not in ["o","n"]:
            print("Saisie incorrecte !")
            continuer = input("Voulez-vous continuer à ajouter de nouveaux roles ? (o pour oui ou n pour non) : ")
        if continuer.lower()[0] == "n":
            termine = True

def recuperer_infos_roles():
    """ Fonction qui récupère les infos de chaque entrée de la table role """
    requeteSQL = """SELECT ID, LIBELLE 
    FROM role"""
    # Exécution de la requête
    curseur.execute(requeteSQL)

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_roles")
        
def recuperer_infos_roles_par_id(id_role):
    """ Fonction qui récupère les infosd'une entrée de la table role par id"""
    requeteSQL = """SELECT LIBELLE 
    FROM role
    WHERE id = ?"""
    # Exécution de la requête
    curseur.execute(requeteSQL, [id_role])

    # Traitement du résultat de la requête
    resultat = curseur.fetchall()
    if resultat:
        return resultat[0][0]
    else:
        print("Pas d'entrée correspondante ! recuperer_infos_roles")    
    
def afficher_roles():
    infos_roles = recuperer_infos_roles()
    liste_ids_roles = []
    print("\n--------\nAffichage des roles\n")
    for role in infos_roles:
        liste_ids_roles.append(role[0])
        print("{} - {}".format(role[0], role[1]))
    print("--------\n")
    return liste_ids_roles

def selectionner_acteurs_et_roles():
    termine = False
    liste_acteurs_et_roles_appaires = []
    while not termine:
        print("Sélectionner un acteur : ")
        liste_ids_acteurs = afficher_acteurs()
        choix_acteur = int(input("Saisir le numéro d'un des acteurs ci-dessus : "))
        while choix_acteur not in liste_ids_acteurs:
            afficher_acteurs()
            print("Sélectionnez dans la liste ci-dessus !")
            choix_acteur = int(input("Saisir le numéro d'un des acteurs ci-dessus : "))
        id_acteur = choix_acteur
        print("Sélectionner un role : ")
        liste_ids_roles = afficher_roles()
        choix_role = int(input("Saisir le numéro d'un des roles ci-dessus (qui correspond au role de {}) : ".format(recuperer_infos_acteurs_par_id(id_acteur))))
        while choix_role not in liste_ids_roles:
            afficher_roles()
            print("Sélectionnez dans la liste ci-dessus !")
            choix_role = int(input("Saisir le numéro d'un des roles ci-dessus (qui correspond au role de {}) : ".format(recuperer_infos_acteurs_par_id(id_acteur))))
        id_role = choix_role
        
        acteur_et_role = recuperer_infos_acteurs_par_id(id_acteur) + " en tant que " + recuperer_infos_roles_par_id(id_role)
        valider_acteur_et_role = input("Validez-vous '{}' (o pour oui ou n pour non) : ".format(acteur_et_role)).lower()[0]
        while valider_acteur_et_role not in ["o","n"]:
           print("Erreur de saisie.")
           valider_acteur_et_role = input("Validez-vous '{}' (o pour oui ou n pour non) : ".format(acteur_et_role)).lower()[0]
        if valider_acteur_et_role == "o":
            liste_acteurs_et_roles_appaires.append([id_acteur, id_role])
        continuer = input("Sélectionner d'autres acteurs et rôles ? (o pour oui ou n pour non) : ").lower()[0]
        while continuer not in ["o","n"]:
            print("Erreur de saisie !")
            continuer = input("Sélectionner d'autres acteurs et rôles ? (o pour oui ou n pour non) : ").lower()[0]
        if continuer == "n":
            termine = True
    return liste_acteurs_et_roles_appaires
            

def inserer_casting(id_film, liste_acteurs_et_roles_appaires):
    for couple_ids_acteur_et_role in liste_acteurs_et_roles_appaires:
        id_acteur = couple_ids_acteur_et_role[0]
        id_role = couple_ids_acteur_et_role[1]
        requeteSQL = """INSERT INTO liste_acteurs(id_film, id_acteur, id_role)
        VALUES (?, ?, ?)"""
        curseur.execute(requeteSQL, [id_film, id_acteur, id_role])    
        connexion.commit()
    
def inserer_support(id_film, type_support, prix, quantite):
    requeteSQL = """INSERT INTO support(id_film, type_support, prix, quantite)
        VALUES (?, ?, ?, ?)"""
    curseur.execute(requeteSQL, [id_film, type_support, prix, quantite])    
    connexion.commit() 

def ajouter_support(id_film): 
    print("--------\nAjout de supports :")
    termine = False
    type_support = "Default"
    while not termine:
        print("--------\nSaisie des infos du support :")
        choix_support = int(input("1 - Pour ajouter des Blue-Ray\n2 - Pour ajouter des DVD\n--------\n0 pour quitter\nVotre choix : "))
        while choix_support not in [0,1,2]:
            print("--------\nSaisie des infos du support :")
            choix_support = int(input("1 - Pour ajouter des Blue-Ray\n2 - Pour ajouter des DVD\n Votre choix : "))
        if choix_support == 2:
            type_support = "DVD"
        elif choix_support == 1:
            type_support = "Blue-Ray"
        elif choix_support == 0:
            print("Ajout de support annulé !")
            return
        choix_prix = float(input("Veuillez saisir le prix (un nombre de la forme xx.xx) : "))
        choix_quantite = int(input("Veuillez saisir la quantité à mettre en stock (un nombre entier) : "))
        prix = choix_prix
        quantite = choix_quantite
        valider_insertion_support = input("Confirmer l'ajout du support : {} pour {}€ avec {} unité(s). Saisir o pour oui, n pour non : ".format(type_support, prix, quantite)).lower()[0]
        if valider_insertion_support == "o":
            inserer_support(id_film, type_support, prix, quantite)
            print("Support ajouté !")
        elif valider_insertion_support == 'n':
            print("Annulation de l'ajout du support")
        continuer = input("Souhaitez-vous continuer à ajouter des supports ? (o pour oui, n pour non) : ").lower()[0]
        while continuer not in ["o", "n"]:
            print("Erreur de saisie !")
            continuer = input("Souhaitez-vous continuer à ajouter des supports ? (o pour oui, n pour non) : ").lower()[0]
        if continuer == "n":
            termine = True
    afficher_supports_disponibles_par_id_film(id_film)

def ajouter_film():
    print("--------\nAjout d'un film")
    saisie = saisir_infos_film()
    if saisie == 'q':
        # Si la saisie consiste à quitter on termine l'ajout
        print("Ajout annulé !\n--------")
        return
    
    # On attribue les infos de la saisie à chaque variable correspondante
    titre, date_sortie, duree, genre, nationalite = saisie
    inserer_film(titre, date_sortie, duree, genre, nationalite)
    
    # On passe à la gestion des ajout d'acteurs et de rôles
    afficher_acteurs()
    ajouter_des_acteurs = input("Y aura-t'il de nouveaux acteurs ? (o pour oui ou n pour non) : ").lower()[0]
    while ajouter_des_acteurs not in ["o","n"]:
        print("Erreur de saisie")
        ajouter_des_acteurs = input("Y aura-t'il de nouveaux acteurs ? (o pour oui ou n pour non) : ").lower()[0]        
    ajouter_des_roles = input("Y aura-t'il de nouveaux rôles ? (o pour oui ou n pour non) : ").lower()[0]
    while ajouter_des_roles not in ["o","n"]:
        print("Erreur de saisie")
        ajouter_des_roles = input("Y aura-t'il de nouveaux rôles ? (o pour oui ou n pour non) : ").lower()[0]
    if ajouter_des_acteurs == "o":
        nouveaux_acteurs()
    if ajouter_des_roles == "o":
        nouveaux_roles()
    
    # On sélectionne les acteurs à ajouter 
    liste_acteurs_et_roles_appaires = selectionner_acteurs_et_roles()
    id_film = recuperer_id_film(titre, date_sortie, duree, genre, nationalite)
    inserer_casting(id_film, liste_acteurs_et_roles_appaires)
    
    # On ajoute les supports
    ajouter_support(id_film)
    print("Film ajouté\n--------")
    afficher_films()

#------------------------------------------------------------------------------
#                  Fonctions pour retirer un film
#------------------------------------------------------------------------------

def supprimer_liste_acteurs(id_film):
    requeteSQL = """DELETE FROM liste_acteurs WHERE id_film = ?"""
    curseur.execute(requeteSQL, [id_film])    
    connexion.commit()
    
def recuperer_ids_support(id_film):
    liste_ids_supports = []
    requeteSQL = """SELECT id FROM support WHERE id_film = ?"""
    curseur.execute(requeteSQL, [id_film]) 
    resultat = curseur.fetchall()
    if resultat:
        # Ajout de l'id de support à la liste
        for i in range(len(resultat)):
            liste_ids_supports.append(resultat[i][0]) 
    else:
        print("Pas d'entrée correspondante ! recuperer_ids_support")
    return liste_ids_supports

def effacer_location_selon_id_support(liste_ids_supports):
    """Fonction qui parcourt une liste d'id de supports 
    et efface les locations utilisant ce support"""
    
    for id_support in liste_ids_supports:
        requeteSQL = """DELETE FROM location WHERE id_support = ?"""
        curseur.execute(requeteSQL, [id_support])    
        connexion.commit()

def effacer_les_supports(liste_ids_supports):
    """Fonction qui parcourt une liste d'id de supports 
    et efface le support correspondant"""
    
    for id_support in liste_ids_supports:
        requeteSQL = """DELETE FROM support WHERE id = ?"""
        curseur.execute(requeteSQL, [id_support])    
        connexion.commit()

def effacer_film(id_film):
    requeteSQL = """DELETE FROM film WHERE id = ?"""
    curseur.execute(requeteSQL, [id_film])    
    connexion.commit()

def retirer_film():
    print("\nRetrait d'un film")
    afficher_films()
    liste_id_films_disponibles = [0]
    for film in recuperer_infos_films():
        # On récupère les indices des films existants
        liste_id_films_disponibles.append(film[0])
    afficher_films()
    print("--------\n0 pour quitter")
    choix = int(input("""Veuillez sélectionner
l'une des options ci-dessus (le numéro du film) : """))
    while choix not in liste_id_films_disponibles:
        afficher_films()
        print("--------\n0 pour quitter")
        print("Le choix doit se faire parmi les propositions ci-dessus !")
        choix = int(input("""Veuillez sélectionner l'une 
des options ci-dessus (le numéro du film) : """))
    if choix == 0: # Si on choisit 0 on quitte la fonction
        print("Retrait annulé !\n--------")
        return
    id_film = choix
    infos_film = recuperer_infos_film_par_id(id_film)
    titre = infos_film[1]
    date_sortie = "({})".format(infos_film[2])
    valider_retrait = input("Confirmer la suppression de {} (o pour oui et n pour non) : ".format(
        titre+" "+date_sortie))
    while valider_retrait.lower()[0] not in ["o","n"]:
        valider_retrait = input("Confirmer la suppression de {} (o pour oui et n pour non) : ".format(
            titre+" "+date_sortie))
    if valider_retrait[0].lower() == 'n':
    # Si on veut annuler on quitte le programme
        print("Retrait annulé !\n--------")
        return
    elif valider_retrait[0].lower() == 'o':
        # On supprime le casting du film
        print("--------\nEffacement du casting")
        supprimer_liste_acteurs(id_film)
        # On récupère la liste des support pour ce film
        liste_ids_supports = recuperer_ids_support(id_film)
        # On efface les locations qui ont loué des supports du film
        print("--------\nEffacement des locations\n--------")
        effacer_location_selon_id_support(liste_ids_supports)
        # On efface les supports
        print("--------\nEffacement des supports")
        effacer_les_supports(liste_ids_supports)
        # On peut maintenant effacer le film
        print("--------\nEffacement du film\n--------")
        effacer_film(id_film)
    print("Film retiré\n--------")

#------------------------------------------------------------------------------
#                       Fonction de menu
#------------------------------------------------------------------------------

def menu():
    resterDansLeMenu = True
    while resterDansLeMenu:
        print("""\n--MENU--\n1 - Afficher la liste des films \n2 - Louer un film
3 - Afficher les locations
4 - Vérification des retours\n5 - Ajouter un film
6 - Retirer un film \n--------\n0 pour quitter""")
        choix = int(input("Veuillez sélectionner l'une des options ci-dessus (le numéro) : "))
        while choix not in [0,1,2,3,4,5,6]:
            print("Le choix doit se faire parmi les propositions ci-dessus !")
            print("""\n1 - Afficher la liste des films \n2 - Louer un film
3 - Afficher les locations
4 - Vérification des retours\n5 - Ajouter un film
6 - Retirer un film \n--------\n0 pour quitter""")
            choix = int(input("Veuillez sélectionner l'une des options ci-dessus (le numéro) : "))
        if choix == 0:
            print("Au revoir !")
            return
        elif choix == 1:
            afficher_films()
        elif choix == 2:
            louer_film()
        elif choix == 3:
            afficher_locations()
        elif choix == 4:
            verifier_retours()
        elif choix == 5:
            ajouter_film()
        elif choix == 6:
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