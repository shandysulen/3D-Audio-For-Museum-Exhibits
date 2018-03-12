import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton,
    QToolTip, QPushButton, QDesktopWidget, QMessageBox, QGridLayout)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Set initial size of window and placement of window
        self.resize(800,400)

        # Set title and icon for window
        self.setWindowTitle('3D Audio For Museum Exhibits')
        self.setWindowIcon(QIcon('images/icon.png'))

        # Center the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Set a grid for widgets to fall in line with
        grid = QGridLayout()
        self.setLayout(grid)

        # Customize ToolTip
        QToolTip.setFont(QFont('SansSerif', 10))

        # Customize play button
        play_btn = QPushButton('Play')
        play_btn.setToolTip('Begin playback of 3D audio')
        play_btn.resize(100,33)

        # Customize stop button
        stop_btn = QPushButton('Stop')
        stop_btn.setToolTip('Stop playback of 3D audio')
        stop_btn.resize(100,33)

        # Customize canvas
        canvas = QPixmap('images/canvas.jpg')
        canvas_lbl = QLabel(self)
        canvas_lbl.setPixmap(canvas)

        # Customize radio buttons
        radio_one = QRadioButton("1")
        radio_one.setChecked(True)
        # radio_one.toggled.connect()

        radio_two = QRadioButton("2")
        # radio_two.toggled.connect()

        radio_three = QRadioButton("3")
        # radio_three.toggled.connect()

        radio_four = QRadioButton("4")
        # radio_four.toggled.connect()

        # Add button widgets to grid
        grid.addWidget(QWidget(), 1, 1, 1, 3) # empty space
        grid.addWidget(canvas_lbl, 2, 1, 3, 3) # <---canvas
        grid.addWidget(QWidget(), 5, 1, 1, 3) # empty space
        grid.addWidget(play_btn, 5, 4) # play button
        grid.addWidget(stop_btn, 5, 5) # stop button
        grid.addWidget(radio_one, 1, 4) # first radio button
        grid.addWidget(radio_two, 2, 4) # second radio button
        grid.addWidget(radio_three, 3, 4) # third radio button
        grid.addWidget(radio_four, 4, 4) # fourth radio button
        grid.addWidget(QWidget(), 1, 5, 4, 1) # empty space

        # Show the window
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure you wish to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':

    # Represents our application and any command-line arguments
    app = QApplication(sys.argv)

    # Create window widget
    w = window()

    # Begin the mainloop execution and assure graceful exiting
    sys.exit(app.exec_())
