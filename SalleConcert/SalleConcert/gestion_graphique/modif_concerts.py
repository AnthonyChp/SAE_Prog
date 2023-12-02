from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QPushButton, QLineEdit

class ModifConcerts(QDialog):
    def __init__(self, data_to_edit, donnees_concerts):
        super().__init__()
        self.donnees_concerts = donnees_concerts

        self.setWindowTitle('Edit Concert')
        self.resize(300, 200)

        self.layout = QVBoxLayout(self)

        # Display labels and line edits for each column
        self.line_edits = []
        for label, value in zip(["ID", "Titre", "Artiste", "Date", "Tarif"], data_to_edit):
            label_widget = QLabel(label)
            line_edit = QLineEdit(value)

            self.layout.addWidget(label_widget)
            self.layout.addWidget(line_edit)

            self.line_edits.append(line_edit)

        # Button to confirm the edits
        self.confirm_button = QPushButton("Confirm Edit")
        self.layout.addWidget(self.confirm_button)

        # Connect the button to the function
        self.confirm_button.clicked.connect(self.accept)

    def get_edited_data(self):
        return [line_edit.text() for line_edit in self.line_edits]
