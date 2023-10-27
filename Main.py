import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextBrowser, QLabel
from Vplayer import Vplayer
from Csv_file import Csv_file

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Glowne Okno")
        self.setGeometry(100, 100, 600, 400)

        csv_widget = Csv_file()
        csv_widget.csv_file()

        csv_label = QLabel(self)
        csv_label.setText(csv_widget.text_browser.toPlainText())
        csv_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        video_widget = Vplayer()
        video_label = QLabel(self)
        video_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        control_widget = QWidget(self)
        control_layout = QVBoxLayout(control_widget)

        start_button = video_widget.start_button
        stop_button = video_widget.stop_button
        restart_button = video_widget.restart_button
        csv_file = csv_widget.csv_file()

        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)
        control_layout.addWidget(restart_button)
        control_layout.addWidget(csv_file)

        main_layout = QVBoxLayout()
        main_layout.addWidget(csv_label)
        main_layout.addWidget(video_widget)
        main_layout.addWidget(control_widget)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec())