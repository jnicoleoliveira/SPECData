# Author: Jasmine Oliveira
# Date: 7/12/2016

import MainWindow

import sys
from PyQt4.QtGui import *

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('specdata')

    main = MainWindow.MainWindow()
    main.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()