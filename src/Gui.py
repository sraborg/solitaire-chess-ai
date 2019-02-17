import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setGeometry(50, 50, 800, 500)
window.setWindowTitle('Solitare Chess AI')

window.show()
sys.exit(app.exec_())