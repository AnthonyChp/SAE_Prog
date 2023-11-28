import mysql.connector

# Fonction pour se connecter à la base de données
def connect():

        connection = mysql.connector.connect(
            host='localhost',
            database='salle_concert',
            user='admin',
            password='admin'
        )

        return connection



# Fonction pour récupérer et afficher les données de la table "spectateurs"
def fetch_and_display_data(connection):

        cursor = connection.cursor()

        # Exécutez votre requête ici
        requete_spec = "SELECT * FROM spectateurs"
        cursor.execute(requete_spec)

        # Récupérez les résultats
        rows = cursor.fetchall()

        # Affichez les résultats
        for row in rows:
            print(row)

        # Fermez le curseur et la connexion
        cursor.close()


# Programme principal
def main():
    connection = connect()

    if connection:
        fetch_and_display_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
