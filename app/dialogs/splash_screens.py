from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocessing import Pool
import time

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')


class LoadingSplashScreen(QSplashScreen):
    def __init__(self, animation, flags):
        # run event dispatching in another thread
        QSplashScreen.__init__(self, QPixmap(), flags)
        self.movie = QMovie(animation)
        self.connect(self.movie, SIGNAL('frameChanged(int)'), SLOT('onNextFrame()'))
        self.movie.start()

    @pyqtSlot()
    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())


# Put your initialization code here
def longInitialization(arg):
    time.sleep(arg)
    return 0


class LoadingProgressScreen():
    def __init__(self, parent=None):
        self.dialog = QProgressDialog("Please Wait", "Cancel", 0, 100)

    def start(self):
        self.dialog.setWindowModality(Qt.WindowModal)
        self.dialog.setAutoReset(True)
        self.dialog.setAutoClose(True)
        self.dialog.setMinimum(0)
        self.dialog.setMaximum(100)
        self.dialog.resize(200, 200)
        self.dialog.setWindowTitle("Progress")
        self.dialog.show()
        self.dialog.setValue(0)
        QApplication.processEvents()


    def next_value(self, value):
        self.dialog.setValue(value)
        QApplication.processEvents()
        #self.dialog.show()

    def set_caption(self,text):
        self.dialog.setLabelText(text)

    def end(self):
        self.dialog.setValue(100)
        time.sleep(2)
        self.dialog.hide()

if __name__ == "__main__":
    import sys, time

    app = QApplication(sys.argv)

    # Create and display the splash screen
    #   splash_pix = QPixmap('a.gif')
    splash = LoadingSplashScreen('a.gif', Qt.WindowStaysOnTopHint)
    #   splash.setMask(splash_pix.mask())
    # splash.raise_()
    splash.show()
    app.processEvents()

    # this event loop is needed for dispatching of Qt events
    initLoop = QEventLoop()
    pool = Pool(processes=1)
    pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
    initLoop.exec_()

    form = Form()
    form.show()
    splash.finish(form)
    app.exec_()
