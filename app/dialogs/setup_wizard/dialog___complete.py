# Author: Jasmine Oliveira
# Date: 5/12/2017

from PyQt4.QtGui import *

from dialog___wizard_window import WizardWindow


class CompletingWindow(WizardWindow):
    def __init__(self):
        super(CompletingWindow, self).__init__(False)

        self.header_txt = "Completing the SPECdata \nSetup Wizard"
        self.body_txt = "\n\nSPECdata has been successfully installed on your computer. \n\n" \
                        "Click Finish to close this wizard.\n\n\n\n\n\n"
        self.launch_after = QCheckBox("Launch SPECdata")
        self.__setup_center_layout()
        self.__setup_buttons()
        self.show()

    def __setup_buttons(self):
        self.rightbtn.setText("Finish")
        self.leftbtn.hide()
        self.rightbtn.clicked.connect(self.finish_btn_action)

    def finish_btn_action(self):
        if self.launch_after.isChecked():
            self.open_next_window()
        else:
            self.close()

    def open_next_window(self):
        from app.dialogs.dialog___main_menu import MainMenu
        self.close()
        window = MainMenu()
        window.show()
        window.exec_()


    def __setup_center_layout(self):
        # Setup header
        header_lbl = QLabel(self.header_txt)
        header_lbl.setMargin(1)
        header_lbl.setStyleSheet(self.header_font)
        header_lbl.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        header_lbl.setWordWrap(True)

        # Setup Body
        body_lbl = QLabel(self.body_txt)
        body_lbl.setWordWrap(True)
        body_lbl.setStyleSheet(self.body_font)
        # Spacer
        spacer = QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Expanding)

        ###########################################
        # Add all to main layout
        ###########################################
        self.center_layout.addWidget(header_lbl, 0, 0)
        self.center_layout.addWidget(body_lbl, 1, 0)
        self.center_layout.addWidget(self.launch_after, 2, 0)
        self.center_layout.addItem(spacer, 3, 0)
        self.center_layout.setSpacing(0)
