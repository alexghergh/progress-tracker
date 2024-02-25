from typing import List

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from app import Graph
from app.task import Task


class GraphUI(QWidget):
    def __init__(self):
        """
        Main Graph UI interface.

        """
        super().__init__()

        self.graph = Graph()

        self.init_ui()

    def init_ui(self):

        # get system color theme
        system_palette = self.palette()
        figure_color = system_palette.window().color().getRgbF()
        text_color = system_palette.text().color().getRgbF()
        bar_color = system_palette.highlight().color().getRgbF()

        # set graph colors
        self.graph.set_color_scheme(figure_color=figure_color,
                                    text_color=text_color,
                                    bar_color=bar_color)

        # get plot canvas
        self.canvas = self.graph.get_canvas()

        # create widgets and embed plot in PyQt
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        self.setLayout(vbox)

        self.show()

    def refresh_data(self, tasks: List[Task]):
        """
        Refresh graph data.

        Args:
            tasks (List[Task]): List of tasks to update in the graph.

        """
        self.graph.update_graph(tasks)
        self.canvas.draw()
