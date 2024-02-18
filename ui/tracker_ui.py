from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout


class TaskTrackerUI(QWidget):
    def __init__(self, tracker):
        super().__init__()

        self.tracker = tracker

        self.init_ui()

    def init_ui(self):
        # Set the layout
        layout = QVBoxLayout(self)

        # Set the window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Simple PyQt App')
        self.show()
