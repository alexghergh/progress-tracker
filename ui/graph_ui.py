from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)
import pyqtgraph as pg


class GraphUI(QWidget):
    def __init__(self):
        """
        Main Graph UI interface.

        """
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # create plot
        self.plot_widget = pg.PlotWidget(self)

        # create widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.plot_widget)

        self.setLayout(vbox)

        self.show()

    def refresh_data(self, tasks):
        """
        Refresh graph data.

        """
        self.plot_widget.clear()

        task_names = [task.name for task in tasks]
        task_currencies = [task.currency for task in tasks]

        bar_chart = pg.BarGraphItem(x=range(len(task_names)),
                                    height=task_currencies, width=0.6,
                                    brush='b')
        self.plot_widget.addItem(bar_chart)

        # Set labels and title
        self.plot_widget.getAxis('bottom').setTicks([[(i, name) for i, name in enumerate(task_names)]])
        self.plot_widget.setLabel('left', 'Steps')
        self.plot_widget.setLabel('bottom', 'Tasks')
        self.plot_widget.setTitle('Task Tracker')
