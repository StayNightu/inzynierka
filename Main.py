import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout

from BBox import BoundingBoxDrawer
from Vplayer import Vplayer
from Csv_file import Csv_file

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Glowne Okno")
        self.setGeometry(100, 100, 600, 400)

        csv_widget = Csv_file()
        bbox_drawer = BoundingBoxDrawer(csv_writer=csv_widget)
        video_widget = Vplayer()
        widget = QWidget()

        csv_widget.text_browser.setFixedSize(250, 250)
        csv_widget.text_browser.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        bbox_drawer.setFixedSize(640, 480)

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        layout = QVBoxLayout(widget)

        top_layout.addWidget(video_widget)
        top_layout.addStretch(1)
        top_layout.addWidget(csv_widget.text_browser)

        layout.addWidget(bbox_drawer)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(layout)
        


        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())