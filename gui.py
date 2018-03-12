import sys
import hrtf
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton,
    QToolTip, QPushButton, QDesktopWidget, QMessageBox, QGridLayout)
from PyQt5.QtGui import QIcon, QFont, QPixmap

class window(QWidget):

    def __init__(self):
        super().__init__()
        self.radio_buttons = []
        self.initUI()

    def hrtfWrapper(self):
        """
        Sets the proper arguments to be passed in to the hrtf function
        """
        radio_selected = 0

        for i in range(len(self.radio_buttons)):
            if self.radio_buttons[i].isChecked():
                radio_selected = i + 1

        fileName = 'audio/RiverStreamAdjusted.wav'
        aIndex = 0
        eIndex = 8

        if radio_selected == 1:
            aIndex = 12
        elif radio_selected == 2:
            aIndex = 24
        elif radio_selected == 3:
            aIndex = 0

        hrtf.hrtf(fileName, aIndex, eIndex)

    def initUI(self):
        """
        Sets up the GUI for the application
        """
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
        play_btn.clicked.connect(self.hrtfWrapper)

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
        self.radio_buttons.append(radio_one)

        radio_two = QRadioButton("2")
        self.radio_buttons.append(radio_two)

        radio_three = QRadioButton("3")
        self.radio_buttons.append(radio_three)

        # Add button widgets to grid
        grid.addWidget(QWidget(), 1, 1, 1, 3) # empty space
        grid.addWidget(canvas_lbl, 2, 1, 3, 3) # <---canvas
        grid.addWidget(QWidget(), 5, 1, 1, 3) # empty space
        grid.addWidget(play_btn, 5, 4) # play button
        grid.addWidget(stop_btn, 5, 5) # stop button
        grid.addWidget(radio_one, 1, 4) # first radio button
        grid.addWidget(radio_two, 2, 4) # second radio button
        grid.addWidget(radio_three, 3, 4) # third radio button
        grid.addWidget(QWidget(), 1, 5, 4, 1) # empty space

        # Show the window
        self.show()

    def closeEvent(self, event):
        """
        Overrides the closeEvent function to ask if the user really wants to quit
        the real-time application
        """
        reply = QMessageBox.question(self, '3D Audio for Museum Exhibits',
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
