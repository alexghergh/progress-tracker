from typing import List

from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app import Task


class IncrementTaskUI(QDialog):
    def __init__(self, tasks: List[Task]):
        """
        Dialog window for increment a task currency.

        Args:
            tasks (List[Task]): List of tasks to choose from.

        """
        super().__init__()

        self.options = [task.name for task in tasks]

        self.init_ui()

    def init_ui(self):
        # set window properties
        self.setWindowTitle("Update Task")
        self.setMinimumWidth(220)
        self.setMaximumWidth(220)
        self.setMinimumHeight(180)
        self.setMaximumHeight(255)

        # create widgets
        self.name_label = QLabel("Task name: ")
        self.task_combobox = QComboBox()
        self.task_combobox.addItems(self.options)

        self.checkbox = QCheckBox("Custom increment")
        self.increment_label = QLabel("Increment: ")
        self.increment_input = QLineEdit(self)
        self.increment_label.setVisible(False)
        self.increment_input.setVisible(False)

        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)

        # set widgets positions
        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.task_combobox)
        vbox.addWidget(self.checkbox)
        vbox.addWidget(self.increment_label)
        vbox.addWidget(self.increment_input)
        vbox.addWidget(self.ok_button)
        vbox.addWidget(self.cancel_button)

        self.setLayout(vbox)

        # connect buttons to actions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # connect checkbox to show/hide custom increment
        self.checkbox.stateChanged.connect(self.toggle_advanced)

    def toggle_advanced(self, state):
        self.increment_label.setVisible(state == 2)
        self.increment_input.setVisible(state == 2)

        if state == 2:
            self.resize(self.width(), self.height() + 75)
        else:
            self.resize(self.width(), self.height() - 75)
