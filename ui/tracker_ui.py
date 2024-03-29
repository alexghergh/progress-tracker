from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QHBoxLayout,
    QMenu,
    QSystemTrayIcon,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from .add_task_ui import AddTaskUI
from .remove_task_ui import RemoveTaskUI
from .increment_task_ui import IncrementTaskUI
from .graph_ui import GraphUI


class TaskTrackerUI(QWidget):
    def __init__(self, tracker, app):
        """
        Main Tracker UI interface.

        """
        super().__init__()

        # task tracker
        self.tracker = tracker

        self.app = app

        self.init_ui()

    def init_ui(self):
        # set window properties
        app_icon = QIcon('resources/images/tracker.png')
        self.setFixedSize(1400, 900)
        self.setWindowTitle("Progress tracker")
        self.setWindowIcon(app_icon)

        # create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(app_icon)

        # create context menu for tray icon
        tray_menu = QMenu(self)
        exit_action = QAction('Exit', self)

        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.hide()

        # create task buttons
        self.add_button = QPushButton("Add task", self)
        self.add_button.setFixedSize(200, 30)
        self.remove_button = QPushButton("Remove a task", self)
        self.remove_button.setFixedSize(200, 30)
        self.increment_button = QPushButton("Update task", self)
        self.increment_button.setFixedSize(200, 30)

        # make buttons clickable by pressing Enter
        self.add_button.setAutoDefault(True)
        self.remove_button.setAutoDefault(True)
        self.increment_button.setAutoDefault(True)

        # create plot
        self.plot_ui = GraphUI()

        # set the layout
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.increment_button)
        hbox.addStretch()
        hbox.addWidget(self.add_button)
        hbox.addStretch()
        hbox.addWidget(self.remove_button)
        hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addWidget(self.plot_ui)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # connect buttons to actions
        self.add_button.clicked.connect(self.add_task_dialog)
        self.remove_button.clicked.connect(self.remove_task)
        self.increment_button.clicked.connect(self.update_task_dialog)

        exit_action.triggered.connect(self.app.quit)
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # handle window close event (minimize to tray)
        self.closeEvent = self.on_close_event

        self.plot_ui.refresh_data(self.tracker.tasks)
        self.show()

    def add_task_dialog(self):
        """
        Add a task through the UI.

        """
        dialog = AddTaskUI()
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

        # refresh graph data
        self.plot_ui.refresh_data(self.tracker.tasks)

    def remove_task(self):
        """
        Remove a task through the UI.

        """
        dialog = RemoveTaskUI(self.tracker.tasks)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            task_name = dialog.task_combobox.currentText()

            if not task_name:
                QMessageBox.warning(self, "Warning", "Name cannot be empty!")
                return

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

        # refresh graph data
        self.plot_ui.refresh_data(self.tracker.tasks)

    def update_task_dialog(self):
        """
        Update a task through the UI.

        """
        dialog = IncrementTaskUI(self.tracker.tasks)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            task_name = dialog.task_combobox.currentText()

            if not task_name:
                QMessageBox.warning(self, "Warning", "Name cannot be empty!")
                return

            increment = dialog.increment_input.text()
            if not increment:
                increment = 1
            else:
                try:
                    increment = int(increment)
                except ValueError:
                    QMessageBox.warning(self, "Warning", "You can only specify numbers as increment!")
                    return

            if increment < 1:
                QMessageBox.warning(self, "Warning", "Can't increment with negative or zero steps!")
                return

            result = self.tracker.increase_task_currency(task_name, increment)
            if not result:
                QMessageBox.warning(self, "Warning", f"Task with name \"{task_name}\" doesn't exist!")
                return

            QMessageBox.information(self, "Success", f"Task \"{task_name}\" updated!")

        # refresh graph data
        self.plot_ui.refresh_data(self.tracker.tasks)

    def tray_icon_activated(self, reason):
        # restore app from system tray icon
        if reason == QSystemTrayIcon.Trigger:
            self.tray_icon.hide()
            self.show()

    def on_close_event(self, event):
        # minimize to tray when closing window
        event.ignore()
        self.hide()
        self.tray_icon.show()
        self.tray_icon.showMessage(
            "Progress tracker",
            "Application minimized to tray",
            QSystemTrayIcon.NoIcon,
            2000, # 2 seconds
        )
