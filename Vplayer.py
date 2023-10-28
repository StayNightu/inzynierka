import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog


class Vplayer(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.playing = False
        self.init_ui()
        self.current_frame = 0
        self.is_first_frame = True

    def init_ui(self):
        self.label = QLabel(self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.restart_button = QPushButton("Odtwórz ponownie", self)
        self.select_video_button = QPushButton("Wybierz plik wideo", self)
        self.next_frame_button = QPushButton("Następna klatka", self)
        self.prev_frame_button = QPushButton("Poprzednia klatka", self)

        button_size = 110
        button_size2 = 40
        self.start_button.setFixedSize(button_size, button_size2)
        self.stop_button.setFixedSize(button_size, button_size2)
        self.restart_button.setFixedSize(button_size, button_size2)
        self.select_video_button.setFixedSize(button_size, button_size2)
        self.next_frame_button.setFixedSize(button_size, button_size2)
        self.prev_frame_button.setFixedSize(button_size, button_size2)

        self.start_button.clicked.connect(self.start_playing)
        self.stop_button.clicked.connect(self.stop_playing)
        self.restart_button.clicked.connect(self.restart_playing)
        self.select_video_button.clicked.connect(self.select_video)
        self.next_frame_button.clicked.connect(self.next_frame)
        self.prev_frame_button.clicked.connect(self.prev_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.select_video_button)
        layout.addWidget(self.next_frame_button)
        layout.addWidget(self.prev_frame_button)
        self.setLayout(layout)

        self.video_path = None
        self.cap = None

    def select_video(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Plik wideo (*.mp4 *.avi *.mkv)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.video_path = selected_files[0]
                self.cap = cv2.VideoCapture(self.video_path)
                if not self.cap.isOpened():
                    print("Error: Nie mozna odtworzyc.")
                    return
                self.current_frame = 0
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                self.is_first_frame = True
                self.start_playing()

    def start_playing(self):
        self.playing = True
        self.timer.start(33)

    def stop_playing(self):
        self.playing = False
        self.timer.stop()

    def restart_playing(self):
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.is_first_frame = True
            self.start_playing()

    def next_frame(self):
        if self.cap is not None:
            self.current_frame += 1
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if self.current_frame >= frame_count:
                self.current_frame = frame_count - 1
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)


    def prev_frame(self):
        if self.cap is not None:
            self.current_frame -= 1
            if self.current_frame < 0:
                self.current_frame = 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)

    def update_frame(self):
        if self.playing and self.cap is not None:
            ret, frame = self.cap.read()

            if frame is not None:
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                self.label.setPixmap(pixmap)

                if self.is_first_frame:
                    self.stop_playing()
                    self.is_first_frame = False

