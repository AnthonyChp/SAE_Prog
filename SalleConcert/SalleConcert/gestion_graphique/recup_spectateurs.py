from PyQt5.QtWidgets import QWidget
import mysql.connector

class DataSpectateurs(QWidget):
    def __init__(self):
        super().__init__()  # Call the __init__ method of the superclass
        self.connexion_bdd = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="salle_concert"
        )
        self.cursor = self.connexion_bdd.cursor()

    def recup_donnees_spectateurs(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_spectateurs_query(self, query, data):
        self.cursor.execute(query, data)
        self.connexion_bdd.commit()
