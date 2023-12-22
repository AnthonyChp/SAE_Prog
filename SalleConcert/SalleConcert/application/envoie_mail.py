"""
.. module:: email_simulation
   :platform: Unix, Windows
   :synopsis: Script de simulation d'envoi d'e-mail pour la confirmation de réservation.

.. moduleauthor:: Gurvan LE PABIC <gurvan.le.pabic@etu.univ-poitiers.fr>

"""

import mysql.connector
from login_dialog import LoginDialog


def simulate_email_sending(email, emplacement, tarif):
    """
    Simule l'envoi d'un e-mail de confirmation de réservation.

    :param email: L'adresse e-mail du spectateur.
    :type email: str
    :param emplacement: L'emplacement réservé par le spectateur.
    :type emplacement: str
    :param tarif: Le tarif de la réservation.
    :type tarif: str
    :return: Aucun
    :rtype: None
    """
    expediteur = "envoiemail.salle_concert.fr"
    sujet = "Confirmation de réservation"
    message = f"Merci d'avoir réservé vos places pour le concert.\n"\
              f"Vous avez réservé la place {emplacement} au tarif de {tarif}.\n"\
              "Nous attendons avec impatience de vous voir au concert!\n"\
              "Cordialement,\nSalle Concert"

    print("Simulation d'envoi de mail :")
    print(f"De : {expediteur}")
    print(f"À : {email}")
    print(f"Sujet : {sujet}")
    print("Message :")
    print(message)

# Connexion à la base de données
connection = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='admin',
    database='salle_concert'
)

cursor = connection.cursor()

# Récupération des informations depuis la table spectateurs
cursor.execute("SELECT email, emplacement, tarif FROM spectateurs")
result = cursor.fetchall()

# Fermeture de la connexion à la base de données
connection.close()

# Exemple d'utilisation avec les données récupérées
for row in result:
    simulate_email_sending(row[0], row[1], row[2])
