# Author: Jasmine Oliveira
# Date: 7/12/2016

import sys
from PyQt4.QtGui import *
from app.dialogs.dialog___main_window import MainWindow     # Import main window


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('specdata')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
