from typing import List, Tuple
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import mplcursors
from sparklines import sparklines

from app.task import Task


class Graph:
    def __init__(self):
        """
        Create a graph.

        """
        # create plot
        self.fig, self.ax = plt.subplots()

        # bar graph settings
        self.bar_settings = {
            'alpha': 1.0,
            'width': 0.5,
            'color': None, # set later
        }
        self.hover_alpha_mouse_on = 1.0
        self.hover_alpha_mouse_off = 0.3

        # hover settings
        self.hover_settings = {
            'ec': 'black',
            'fc': 'lightblue',
            'boxstyle': 'round,pad=0.3'
        }

        # create mock bars for now, recreated on update
        self.bars = self.ax.bar([], [], **self.bar_settings)

        # connect mplcursors to the figure
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)

        self.ax.autoscale()

    def get_canvas(self):
        """
        Get a QTAgg Canvas backend of the figure.

        """
        return FigureCanvas(self.fig)

    def set_color_scheme(self,
                         figure_color: Tuple,
                         text_color: Tuple,
                         bar_color: Tuple):
        """
        Update the color scheme of the graph.

        Args:
            figure_color (Tuple): Color of graph figure.
            text_color (Tuple): Color of text inside the graph.
            bar_color (Tuple): Color of the bars inside the graph.

        """
        self.fig.set_facecolor(figure_color)
        self.ax.set_facecolor(figure_color)

        # ignore top and right spines
        self.ax.spines['top'].set_color(figure_color)
        self.ax.spines['right'].set_color(figure_color)

        self.ax.spines['bottom'].set_color(text_color)
        self.ax.spines['left'].set_color(text_color)

        self.ax.tick_params(axis='x', colors=text_color)
        self.ax.tick_params(axis='y', colors=text_color)

        self.bar_settings['color'] = bar_color

    # graph bar hover action
    def _on_motion(self, event):
        if event.xdata is not None and event.ydata is not None:
            # reset alpha for all bars
            for bar in self.bars:
                bar.set_alpha(self.hover_alpha_mouse_off)

            hovering = False
            # highlight the bar under the cursor (if any)
            for bar in self.bars:
                if bar.contains(event)[0]:
                    hovering = True
                    bar.set_alpha(self.hover_alpha_mouse_on)
                    break

            # reset alpha for all bars, if no bar hovered
            if hovering is False:
                for bar in self.bars:
                    bar.set_alpha(self.hover_alpha_mouse_on)

    def get_relative_time(self, timestamp):
        now = datetime.now()
        delta = now - datetime.fromisoformat(timestamp)

        # calculate the difference in months, days, hours and minutes
        days = delta.days
        months, days = divmod(days, 30)
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if months > 0:
            if months == 1:
                return '1 month ago'
            else:
                return f'{months} months ago'
        elif days > 0:
            if days == 1:
                return '1 day ago'
            else:
                return f'{days} days ago'
        elif hours > 0:
            if hours == 1:
                return '1 hour ago'
            else:
                return f'{hours} hours ago'
        elif minutes > 0:
            if minutes == 1:
                return 'a minute ago'
            else:
                return f'{minutes} minutes ago'
        else:
            return 'just now'

    def get_history_hover(self, task: Task):
        # list elemnts, joined at the end
        text = []

        # add sparkline history
        text += sparklines([hist['total_currency'] for hist in reversed(task.history)])

        # add relative timestamps
        text += ['', 'History:']
        text += ['(' + str(hist['total_currency']) + ') ' + self.get_relative_time(hist['timestamp']) for hist in task.history]

        return '\n'.join(text)

    def update_graph(self, tasks: List[Task]):
        """
        Update the graph details.

        Args:
            tasks (List[Task]): List of tasks to graph.

        """
        # clear ax
        self.ax.cla()

        # get tasks
        task_names = [task.name for task in tasks]
        task_currencies = [task.currency for task in tasks]

        # create the bars
        self.bars = self.ax.bar(task_names, task_currencies, **self.bar_settings)

        # add interactive cursor for the bars
        cursor = mplcursors.cursor(self.bars,
                                   hover=mplcursors.HoverMode.Transient)

        # display task history on hover
        def on_add(sel):
            index = sel.index
            sel.annotation.get_bbox_patch().set(**self.hover_settings)
            sel.annotation.set_text(self.get_history_hover(tasks[index]))

        # connect hover tooltip
        cursor.connect('add', on_add)
