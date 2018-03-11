import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt.QtGui import QIcon

if __name__ == '__main__':

    # Represents our application and any command-line arguments
    app = QApplication(sys.argv)

    # Create window widget
    window = QWidget()

    # Set initial size of window and placement of window
    window.setGeometry(200,200,1500,750)

    # Set title for window
    window.setWindowTitle('3D Audio For Museum Exhibits')

    # Set window icon

    # Show the window
    window.show()

    # Begin the mainloop execution and assure graceful exiting
    sys.exit(app.exec_())
