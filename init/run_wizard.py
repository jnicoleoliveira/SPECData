# Author: Jasmine Oliveira
# Date: 5/17/2017
# run_wizard.py
# Setup Wizard  executable file
# Driver

import sys

from PyQt4.QtGui import *

from app.dialogs.setup_wizard.main_window import MainWindow  # Import main window


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('setup_wizard')
    app.setQuitOnLastWindowClosed(True)
    # app.setStyle('windows')
    window = MainWindow()
    window.show()
    window.start_main_menu()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
