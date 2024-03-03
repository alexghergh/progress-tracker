import os
import sys
import argparse
from functools import partial

from PyQt5.QtWidgets import QApplication

from app import TaskTracker
from ui import TaskTrackerUI


def get_local_save_file(file_name='tracker.json'):
    xdg_data_home = os.getenv('XDG_DATA_HOME')

    if xdg_data_home:
        save_dir = xdg_data_home
    else:
        home = os.path.expanduser('~')
        save_dir = os.path.join(home, '.local', 'share')

    save_file = os.path.join(save_dir, file_name)
    if not os.path.exists(save_file):
        open(save_file, 'a').close()

    return save_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save-file', help='Tracker json file.', type=str)

    args = parser.parse_args()

    # construct the Qt app
    app = QApplication(sys.argv)

    # open tracker file and import tasks
    if (save_file := args.save_file) is None:
        save_file = get_local_save_file()
    tracker = TaskTracker.import_from_json(save_file)

    # construct the main view
    tracker_app = TaskTrackerUI(tracker, app)

    app.aboutToQuit.connect(partial(tracker.export_to_json, save_file))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
