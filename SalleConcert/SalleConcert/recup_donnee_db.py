import mysql.connector
from mysql.connector.connection import MySQLConnection

def connect() -> MySQLConnection:
    """
    Établit une connexion à la base de données MySQL.

    Returns:
        MySQLConnection: Un objet de connexion à la base de données MySQL.
        
    Raises:
        mysql.connector.Error: En cas d'échec de la connexion à la base de données.
    """
    connection = mysql.connector.connect(
        host='localhost',
        database='salle_concert',
        user='admin',
        password='admin'
    )
    return connection

def fetch_and_display_data(connection: MySQLConnection) -> None:
    """
    Récupère et affiche toutes les données de la table "spectateurs".

    Args:
        connection (MySQLConnection): Un objet de connexion à la base de données MySQL.
        
    Raises:
        mysql.connector.Error: En cas d'erreur lors de l'exécution de la requête SQL.
    """
    cursor = connection.cursor()

    # Exécutez votre requête SQL ici
    requete_spec = "SELECT * FROM spectateurs"
    cursor.execute(requete_spec)

    # Récupérez les résultats
    rows = cursor.fetchall()

    # Affichez les résultats
    for row in rows:
        print(row)

    # Fermez le curseur
    cursor.close()

def main() -> None:
    """
    Fonction principale pour démontrer la connexion à la base de données et la récupération des données.
    
    Raises:
        mysql.connector.Error: En cas d'échec de la connexion ou de l'exécution de la requête SQL.
    """
    try:
        # Établir la connexion à la base de données
        connection = connect()

        # Vérifier si la connexion a réussi
        if connection:
            # Récupérer et afficher les données de la table "spectateurs"
            fetch_and_display_data(connection)

            # Fermer la connexion
            connection.close()

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        # Gérer l'erreur (par exemple, en affichant un message d'erreur ou en enregistrant des journaux)

if __name__ == "__main__":
    main()
