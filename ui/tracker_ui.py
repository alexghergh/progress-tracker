from PyQt5.QtWidgets import (
    QDialog,
    QInputDialog,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from .add_task_ui import AddTaskUI


class TaskTrackerUI(QWidget):
    def __init__(self, tracker):
        """
        Main Tracker UI interface.

        """
        super().__init__()

        # task tracker
        self.tracker = tracker

        self.init_ui()

    def init_ui(self):
        # set window properties
        self.setFixedSize(300, 300)
        self.setWindowTitle("Progress tracker")

        # create task buttons
        self.add_button = QPushButton("Add task", self)
        self.remove_button = QPushButton("Remove a task", self)

        # set the layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.add_button)
        vbox.addWidget(self.remove_button)

        self.setLayout(vbox)

        # connect buttons to actions
        self.add_button.clicked.connect(self.add_task_dialog)
        self.remove_button.clicked.connect(self.remove_task)
        self.show()

    def add_task_dialog(self):
        """
        Add a task through the UI.

        """
        dialog = AddTaskUI(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            task_name = dialog.name_input.text()
            currency_name = dialog.currency_input.text()

            if not task_name:
                QMessageBox.warning(self, "Warning", "Name cannot be empty!")
                return

            result = self.tracker.create_and_add_task(task_name, currency_name)
            if not result:
                QMessageBox.warning(self, "Warning", f"Task with name \"{task_name}\" already exists!")
                return

            QMessageBox.information(self, "Success", f"Task \"{task_name}\" added!")

    def remove_task(self):
        """
        Remove a task through the UI.

        """
        task_name, ok_pressed = QInputDialog.getText(self, "Remove task", "Task name")
        if ok_pressed and task_name:

            # ask for confirmation before removing the task
            reply = QMessageBox.question(self, "Confirmation",
                                         f"Are you sure you want to remove the task \"{task_name}\"?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                result = self.tracker.remove_task(task_name)
                if result:
                    QMessageBox.information(self, "Success", f"Task \"{task_name}\" removed!")
                else:
                    QMessageBox.warning(self, "Warning", f"No such task \"{task_name}\"!")
            else:
                return
