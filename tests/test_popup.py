import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()


        # Créer un bouton
        btn = QPushButton('Cliquez-moi', self)
        btn.clicked.connect(self.showDialog)

        # Définir la disposition de la fenêtre
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Application PyQt Basique')
        self.show()

    def showDialog(self):
        # Afficher une boîte de dialogue
        QMessageBox.information(self, 'Message', 'Fenêtre pop-up affichée!')


def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
