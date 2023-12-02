import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application à onglets")

        # Créer un widget central avec un layout vertical
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Créer un onglet
        self.tabs = QTabWidget(self)
        layout.addWidget(self.tabs)

        # Ajouter le premier onglet
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Onglet 1")
        self.tab1_layout = QVBoxLayout(self.tab1)
        label1 = QLabel("Contenu de l'onglet 1", self)
        self.tab1_layout.addWidget(label1)

        # Ajouter le deuxième onglet
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Onglet 2")
        self.tab2_layout = QVBoxLayout(self.tab2)
        label2 = QLabel("Contenu de l'onglet 2", self)
        self.tab2_layout.addWidget(label2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
