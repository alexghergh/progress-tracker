import json

from .task import Task


class TaskTracker:
    def __init__(self):
        """
        Create a task tracker.

        """
        self.tasks = []

    def create_and_add_task(self, task_name: str, currency_name: str) -> bool:
        """
        Create and add a task to the task tracker. Can fail if duplicates are
        present.

        Args:
            task_name (str): Task name.
            currency_name (str): Currency name.

        Returns (bool): Whether the task was added.

        """
        if not isinstance(task_name, str):
            raise ValueError("Task name must be string!")
        if currency_name and not isinstance(currency_name, str):
            raise ValueError("Currency name must be string!")
        if currency_name:
            return self.add_task(Task(task_name, currency_name))
        return self.add_task(Task(task_name))

    def add_task(self, task: Task) -> bool:
        """
        Add a task to the task tracker. Can fail if duplicates are present.

        Args:
            task (Task): Task to add.

        Returns (bool): Whether the task was added.

        """
        if not isinstance(task, Task):
            raise ValueError("Invalid task object.")
        for t in self.tasks:
            if t.name == task.name:
                return False
        self.tasks.append(task)
        return True

    def remove_task(self, task_name: str) -> bool:
        """
        Remove task from task tracker.

        Args:
            task_name (str): Task to remove.

        Returns (bool): Whether the task was removed.

        """
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                return True
        return False

    def increase_task_currency(self, task_name: str, step: int=1) -> bool:
        """
        Increase the currency of a task by 'step' steps.

        Args:
            task_name (str): Name of the task.
            step (int): Amount of increase in task currency.

        Returns: Whether the task's currency was increased.

        """
        for task in self.tasks:
            if task.name == task_name:
                task.increment(step)
                return True
        return False

    def export_to_json(self, json_file_path: str) -> None:
        """
        Export task tracker to json file.

        Args:
            json_file_path (str): Path to JSON file.

        """
        with open(json_file_path, 'w') as file:
            json.dump(
                [task.export_to_dict() for task in self.tasks],
                file, indent=2)

    @classmethod
    def import_from_json(cls, json_file_path: str) -> 'TaskTracker':
        """
        Import and create task tracker from json file.

        Args:
            json_file_path (str): Path to JSON file.

        """
        tracker = cls()
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for task in data:
                tracker.add_task(Task.import_from_dict(task))
        return tracker
