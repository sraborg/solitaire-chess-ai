import sys
from PyQt5.QtCore import QSize, Qt, QPoint
#from PyQt5.QtGui import *
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QAction, QPushButton, QDialog, QMdiArea, QVBoxLayout, QDialogButtonBox
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QComboBox, QFileDialog
from PyQt5.QtWidgets import QGroupBox, QFormLayout, QGridLayout, QSpinBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from Chessboard import Chessboard as cb
from Chessboard import Piece
from SearchStrategy import *
from SearchAgent import SearchAgent
from ObserverInterface import *


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()

        # Add Models / Configure AI
        self.chessboard = None
        self.agent = SearchAgent()
        self.position = {}

        # Icons
        self.pawnIcon = QIcon('./assets/icons/pawn.png')
        self.queenIcon = QIcon('./assets/icons/queen.png')
        self.kingIcon = QIcon('./assets/icons/king.png')
        self.rookIcon = QIcon('./assets/icons/rook.png')
        self.bishopIcon = QIcon('./assets/icons/bishop.png')
        self.knightIcon = QIcon('./assets/icons/knight.png')

        self.layout = QVBoxLayout()

        self.initUI()

    ##
    #   Draws Window GUI

    def initUI(self):
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle('Solitare Chess AI')
        # self.setWindowIcon(QIcon('pic.png'))

        self.mdi = QMdiArea()


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
        # fileMenu.addAction(loadAction)
        # fileMenu.addAction(saveAction)
        fileMenu.addAction(quitAction)

        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close_application)

        search_combo_box = QComboBox(self)
        search_combo_box.addItem('Depth First Search')
        search_combo_box.addItem('Breadth First Search')
        search_combo_box.addItem('Iterative Deepening Search')
        search_combo_box.setMinimumContentsLength(search_combo_box.minimumContentsLength())
        search_combo_box.resize(search_combo_box.minimumSizeHint())
        search_combo_box.activated[int].connect(self._set_search_strategy)

        search_btn = QPushButton("Search!", self)
        search_btn.clicked.connect(self._search)
        search_btn.resize(search_btn.minimumSizeHint())
        #btn.move(200, 5)

        self.toolbar = self.addToolBar('Search')
        self.toolbar.addWidget(search_combo_box)
        self.toolbar.addWidget(search_btn)

        self.chessboard_table_widget = QTableWidget()
        self.layout.addWidget(self.chessboard_table_widget)
        self.setCentralWidget(self.mdi)
        self.mdi.setLayout(self.layout)
        self.show()

    ##
    #   Signal: Responds to File action "new board"
    #   Prompts for dimensions and then creates board based on response
    def _new_board(self):
        # https://stackoverflow.com/questions/17512542/getting-multiple-inputs-from-qinputdialog-in-qtcreator
        rows = 3
        columns = 3

        dialog = NewBoardDialog(self)

        if dialog:
            rows, columns = dialog.getResults()
            #print(rows, columns)
            new_board = cb(rows, columns)
            new_board.register_observer(self)
            self.chessboard = new_board
            self._create_board(rows, columns)

    ##
    #   Draws Board and Stores Positioning information

    def _create_board(self, rows_, columns_):
        self.chessboard_table_widget.setParent(None) # Remove Old
        self.chessboard_table_widget = QTableWidget()
        self.chessboard_table_widget.setRowCount(rows_)
        self.chessboard_table_widget.setColumnCount(columns_)
        self.chessboard_table_widget.horizontalHeader().setDefaultSectionSize(125);
        self.chessboard_table_widget.verticalHeader().setDefaultSectionSize(125);
        self.chessboard_table_widget.setIconSize(QSize(100,100))
        self.chessboard_table_widget.horizontalHeader().hide()
        self.chessboard_table_widget.verticalHeader().hide()
        self.chessboard_table_widget.itemClicked.connect(self._chessboard_click)

        # Create Table Cells
        i = 0
        for r in range(rows_):
            for c in range(columns_):
                #t = str(c) + " " + str(r)
                cell = QTableWidgetItem()
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                if r % 2:
                    if i % 2:
                        cell.setBackground(QColor(150, 150, 150))
                else:
                    if not i % 2:
                        cell.setBackground(QColor(150, 150, 150))

                self.chessboard_table_widget.setItem(r, c, cell)
                i = i + 1

        self.layout.addWidget(self.chessboard_table_widget)
        self.resize(self.sizeHint())

        # Hash Positions
        for c in range(columns_):
            for r in range(rows_):
                # Find "index" from Row / Column notation
                max_rows = self.chessboard_table_widget.rowCount()
                max_columns = self.chessboard_table_widget.columnCount()
                row2 = max_rows - r - 1
                position = c + row2 * max_columns + 1

                key = str(r) + "x" + str(c)

                #print('key', key, 'position', position)
                self.position[key] = position
                self.position[position] = (r,c)

    def _load_board(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        pass

    def _save_board(self):
        pass

    ##
    #   Signal: Responds to changes from Strategy Combo Box
    #   Determines which Search Stategy to use

    def _set_search_strategy(self, strategy_):
        if strategy_ == 0:
            self.agent.strategy = DepthFirstSearch()
        elif strategy_ == 1:
            self.agent.strategy = BreadthFirstSearch()
        elif strategy_ == 2:
            self.agent.strategy = IterativeDeepeningSearch()

    ##
    #   Runs Search on Current Board

    def _search(self):
        self.agent.chessboard = self.chessboard
        self.agent.search()
        print(self.agent.solutions)

    ##
    #   Signal: Responds to "Quit Action"
    #   Closes Application

    def close_application(self):
        sys.exit()

    ##
    #   Signal: Responds to Clicking on Table
    #   Lets user add/remove pieces from the board

    def _chessboard_click(self, item_):


        #max_rows = self.chessboard_table_widget.rowCount()
        #max_columns = self.chessboard_table_widget.columnCount()

        row = self.chessboard_table_widget.currentRow()
        column = self.chessboard_table_widget.currentColumn()
        #        row2 = max_rows - row - 1
        #position = column + row2 * \
        #        max_columns + 1


        key = str(row) + 'x' + str(column)
        position = self.position.get(key)
        item = self.chessboard_table_widget.item(row, column)
        print(item)

        dialog = AddRemovePieceDialog(self)

        piece = dialog.getResults()

        if piece == "Bishop":
            self.chessboard.add_piece(self.position.get(key), Piece.BISHOP)
        elif piece == "King":
            self.chessboard.add_piece(self.position.get(key), Piece.KING)
        elif piece == "Knight":
            self.chessboard.add_piece(self.position.get(key), Piece.KNIGHT)
        elif piece == "Queen":
            self.chessboard.add_piece(self.position.get(key), Piece.QUEEN)
        elif piece == "Pawn":
            self.chessboard.add_piece(self.position.get(key), Piece.PAWN)
            #item.setIcon(self.pawnIcon)
        elif piece == "Rook":
            self.chessboard.add_piece(self.position.get(key), Piece.ROOK)
        else:
            self.chessboard.remove_piece(self.position.get(key))
        pass

    def update_board(self, piece_positions):
        for position, piece in piece_positions:
            self.update_board_position(piece, position)

    def update_board_position(self, piece, position):
        print(position)
        print(self.position.get(position))

        r, c = self.position.get(position)
        item = self.chessboard_table_widget.item(r,c)

        if piece == Piece.BISHOP:
            item.setIcon(self.bishopIcon)
        elif piece == Piece.KING:
            item.setIcon(self.kingIcon)
        elif piece == Piece.KNIGHT:
            item.setIcon(self.knightIcon)
        elif piece == Piece.QUEEN:
            item.setIcon(self.queenIcon)
        elif piece == Piece.PAWN:
            item.setIcon(self.pawnIcon)
        elif piece == Piece.ROOK:
            item.setIcon(self.rookIcon)
        elif piece is None:
            item.setIcon(QIcon())

    def update_observer(self, subject_):
        self.update_board(self.chessboard.pieces())
        print(self.chessboard.pieces())
        pass

##
#   Class
class NewBoardDialog(QDialog):

    def __init__(self, parent):
        super(NewBoardDialog, self).__init__(parent)

        self.createFormGroupBox()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.form_group_box)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)


        self.setWindowTitle("Board Dimensions")

    def createMenu(self):
        pass

    def createFormGroupBox(self):
        self.form_group_box = QGroupBox("Form layout")
        self.row_spin_box = QSpinBox()
        self.row_spin_box.setMinimum(1)
        self.row_spin_box.setMaximum(10)
        self.row_spin_box.setValue(4)
        self.column_spin_box = QSpinBox()
        self.column_spin_box.setMinimum(1)
        self.column_spin_box.setMaximum(10)
        self.column_spin_box.setValue(4)
        layout = QFormLayout()
        layout.addRow(QLabel("Rows:"), self.row_spin_box)
        layout.addRow(QLabel("Columns:"), self.column_spin_box)
        self.form_group_box.setLayout(layout)

    def getResults(self):
        result = self.exec_() # Halt Program
        if result:
            return self.row_spin_box.value(), self.column_spin_box.value()
        else:
            return None


class AddRemovePieceDialog(QDialog):

    def __init__(self, parent):
        super(AddRemovePieceDialog, self).__init__(parent)

        #self.createFormGroupBox()

        self.form_group_box = QGroupBox("Form layout")
        self.piece_combo_box = QComboBox()
        self.piece_combo_box.addItem("None")
        self.piece_combo_box.addItem("Bishop")
        self.piece_combo_box.addItem("King")
        self.piece_combo_box.addItem("Knight")
        self.piece_combo_box.addItem("Pawn")
        self.piece_combo_box.addItem("Queen")
        self.piece_combo_box.addItem("Rook")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.piece_combo_box)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)



        self.setWindowTitle("Add/Remove Piece")

    def createMenu(self):
        pass

    def createFormGroupBox(self):

        layout = QFormLayout()
        self.form_group_box.setLayout(layout)

    def getResults(self):
        result = self.exec_() # Halt Program
        if result:
            return self.piece_combo_box.currentText()
        else:
            return None


def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

run()

