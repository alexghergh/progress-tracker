from typing import List

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app import Task


class RemoveTaskUI(QDialog):
    def __init__(self, tasks: List[Task]):
        """
        Dialog window for removing a task.

        Args:
            tasks (List[Task]): List of tasks to choose from.

        """
        super().__init__()

        self.options = [task.name for task in tasks]

        self.init_ui()

    def init_ui(self):
        # set window properties
        self.setWindowTitle("Remove Task")
        self.setMinimumWidth(220)
        self.setMaximumWidth(220)
        self.setMinimumHeight(180)
        self.setMaximumHeight(255)

        # create widgets
        self.name_label = QLabel("Task name: ")
        self.task_combobox = QComboBox()
        self.task_combobox.addItems(self.options)

        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)

        # set widgets positions
        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.task_combobox)
        vbox.addWidget(self.ok_button)
        vbox.addWidget(self.cancel_button)

        self.setLayout(vbox)

        # connect buttons to actions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
