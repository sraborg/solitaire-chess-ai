import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QComboBox, QFileDialog


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Solitare Chess AI')
        # self.setWindowIcon(QIcon('pic.png'))


        newAction = QAction('&New Board', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self._new_board)

        loadAction = QAction('&Load Board', self)
        loadAction.setShortcut('Ctrl+L')
        loadAction.triggered.connect(self._load_board)

        saveAction = QAction('&Save Board', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self._save_board)

        quitAction = QAction('&Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('Quit Application')
        quitAction.setMenuRole(QAction.NoRole)
        quitAction.triggered.connect(self.close_application)
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(quitAction)

        comboBox = QComboBox(self)
        comboBox.addItem('Depth First Search')
        comboBox.addItem('Breadth First Search')
        comboBox.addItem('Iterative Deepening Search')
        comboBox.setMinimumContentsLength(comboBox.minimumContentsLength())
        comboBox.resize(comboBox.minimumSizeHint())

        comboBox.move(5, 5)

        comboBox.activated[str].connect(self._set_search_strategy)

        btn = QPushButton("Search!", self)
        btn.clicked.connect(self._search)
        btn.resize(btn.minimumSizeHint())
        btn.move(200, 5)

        self.create_gui()

    def create_gui(self):
        self.show()

    def _new_board(self):
        pass

    def _load_board(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        pass

    def _save_board(self):
        pass

    def _set_search_strategy(self):
        pass

    def _search(self):
        pass
    def close_application(self):
        sys.exit()
        

def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

run()

