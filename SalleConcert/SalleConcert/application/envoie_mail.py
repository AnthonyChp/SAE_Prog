import smtplib
from email.message import EmailMessage

def send_email(subject, body):
    gmail_user = 'votre_email@gmail.com'
    gmail_password = 'votre_mot_de_passe'

    msg = EmailMessage()
    msg['From'] = gmail_user
    msg['To'] = 'destination@example.com'
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)

        server.send_message(msg)
        print("E-mail envoyé avec succès!")

    except Exception as e:
        print("Erreur lors de l'envoi de l'e-mail:", e)

    finally:
        server.quit()

# Exemple d'utilisation pour envoyer un e-mail après une réservation
subject = 'Récapitulatif de votre réservation'
body = 'Bonjour,\n\nMerci d\'avoir réservé pour le concert. Voici le récapitulatif de votre commande.'

# Appel de la fonction send_email avec le sujet et le corps du message
send_email(subject, body)