from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AddTaskUI(QDialog):
    def __init__(self, parent):
        """
        Dialog window for adding a task.

        """
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        # set window properties
        self.setWindowTitle("Add Task")
        self.setFixedSize(220, 200)

        # create widgets
        self.name_label = QLabel("Task name", self)
        self.currency_label = QLabel("Currency name", self)
        self.name_input = QLineEdit(self)
        self.currency_input = QLineEdit(self)
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)

        # set widgets positions
        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_input)
        vbox.addWidget(self.currency_label)
        vbox.addWidget(self.currency_input)
        vbox.addWidget(self.ok_button)
        vbox.addWidget(self.cancel_button)

        self.setLayout(vbox)

        # connect buttons to actions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
