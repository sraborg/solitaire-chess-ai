import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Solitare Chess AI')
        # self.setWindowIcon(QIcon('pic.png'))
        self.create_gui()

        quitAction = QAction('&Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Quit Application')
        quitAction.setMenuRole(QAction.NoRole)
        quitAction.triggered.connect(self.close_application)
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(quitAction)

    def create_gui(self):
        self.show()

    def close_application(self):
        sys.exit()
        

def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

run()

