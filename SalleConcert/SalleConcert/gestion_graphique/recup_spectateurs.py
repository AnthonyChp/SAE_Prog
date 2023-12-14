"""
.. module:: recup_spectateurs
   :platform: Unix, windows
   :synopsis: Module pour récupérer les données de la table spectateurs dans la base de données

.. moduleauthor:: Bauwens Matthieu <matthieu.bauwens@etu.univ-poitiers.fr>


"""

from PyQt5.QtWidgets import QWidget
import mysql.connector

class DataSpectateurs(QWidget):

    """
    La classe DataSpectateurs permet de récupérer et d'exécuter des requêtes liées à la table des spectateurs dans la base de données.

    Cette classe utilise la bibliothèque `mysql.connector` pour la connexion à la base de données MySQL.

    :ivar connexion_bdd: L'objet de connexion à la base de données.
    :vartype connexion_bdd: mysql.connector.connection.MySQLConnection
    :ivar cursor: Le curseur utilisé pour exécuter des requêtes SQL.
    :vartype cursor: mysql.connector.cursor.MySQLCursor
    """

    def __init__(self):

        """
        Initialise une nouvelle instance de la classe DataSpectateurs et établit la connexion à la base de données.

        La connexion est établie avec les paramètres spécifiés (hôte, utilisateur, mot de passe, base de données).
        """

        super().__init__()  # Call the __init__ method of the superclass
        self.connexion_bdd = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="salle_concert"
        )
        self.cursor = self.connexion_bdd.cursor()

    def recup_donnees_spectateurs(self, query):

        """
        Récupère les données des spectateurs en exécutant la requête spécifiée.

        :param query: La requête SQL SELECT à exécuter.
        :type query: str
        :return: Les données des spectateurs sous forme de liste de tuples.
        :rtype: list
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_spectateurs_query(self, query, data):

        """
        Exécute une requête SQL sur la table des spectateurs avec des données spécifiées.

        :param query: La requête SQL à exécuter.
        :type query: str
        :param data: Les données à utiliser dans la requête.
        :type data: tuple
        """
        
        self.cursor.execute(query, data)
        self.connexion_bdd.commit()
