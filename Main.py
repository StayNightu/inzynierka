import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextBrowser, QLabel, \
    QSizePolicy, QHBoxLayout
from PyQt6.QtGui import QPixmap

from BBox import BoundingBoxDrawer
from Vplayer import Vplayer
from Csv_file import Csv_file

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Glowne Okno")
        self.setGeometry(100, 100, 600, 400)

        # Create instances of your widgets
        csv_widget = Csv_file()
        video_widget = Vplayer()
        widget = QWidget()

        # Adjust the size and policies for the csv_widget's QTextBrowser
        csv_widget.text_browser.setFixedSize(250, 250)
        csv_widget.text_browser.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Create main layout and sub-layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        layout = QVBoxLayout(widget)

        # Add video widget and a stretchable space in the top layout.
        # The stretchable space pushes the CSV display to the right.
        top_layout.addWidget(video_widget)
        top_layout.addStretch(1)
        top_layout.addWidget(csv_widget.text_browser)

        box_drawer = BoundingBoxDrawer()
        box_drawer.setPixmap(QPixmap("test_image.jpg"))  # Załaduj przykładowy obraz.
        box_drawer.setFixedSize(QSize(640, 480))

        layout.addWidget(box_drawer)



        # Add top_layout to main_layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(layout)
        # Other widgets can be added to the main_layout here, if needed

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())