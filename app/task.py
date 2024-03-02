from datetime import datetime


class Task:
    def __init__(self, name: str, currency_name="steps"):
        """
        Create a task.

        Args:
            name (str): Name of task.
            currency_name (str): Currency name of task. Defaults to 'steps'.

        """
        if not isinstance(name, str):
            raise ValueError("'name' must be string!")
        self.name = name

        if not isinstance(currency_name, str):
            raise ValueError("'currency_name' must be string!")
        self.currency_name = currency_name

        self.currency = 0
        self.history = []

    def increment(self, step: int=1) -> None:
        """
        Increment the currency of the task by 'step' steps, and add timestamp to
        beggining of history.

        Args:
            step (int): Increment by these many steps. Defaults to 1.

        """
        self.currency += step
        timestamp = datetime.now().isoformat()
        self.history.insert(0, {
            "total_currency": self.currency,
            "timestamp": timestamp
        })

    def export_to_dict(self) -> dict:
        """
        Export task to dict.

        """
        return {
            "name": self.name,
            "currency_name": self.currency_name,
            "currency": self.currency,
            "history": self.history
        }

    @classmethod
    def import_from_dict(cls, other: dict) -> 'Task':
        """
        Import and create task from dict.

        Args:
            other (dict): Dictionary to import from.

        """
        task = cls(other["name"], other["currency_name"])
        task.currency = other["currency"]
        task.history = other["history"]
        return task
