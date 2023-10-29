import cv2
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog


class Vplayer(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = None
        self.playing = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_playing)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_playing)
        layout.addWidget(self.stop_button)

        self.restart_button = QPushButton("Odtwórz ponownie", self)
        self.restart_button.clicked.connect(self.restart_playing)
        layout.addWidget(self.restart_button)

        self.next_frame_button = QPushButton("Następna klatka", self)
        self.next_frame_button.clicked.connect(self.next_frame)
        layout.addWidget(self.next_frame_button)

        self.prev_frame_button = QPushButton("Poprzednia klatka", self)
        self.prev_frame_button.clicked.connect(self.prev_frame)
        layout.addWidget(self.prev_frame_button)

        self.select_video_button = QPushButton("Wybierz plik wideo", self)
        self.select_video_button.clicked.connect(self.select_video)
        layout.addWidget(self.select_video_button)

        self.setLayout(layout)

    def select_video(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Plik wideo (*.mp4 *.avi *.mkv)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.video_path = selected_files[0]
                self.load_video()

    def load_video(self):
        if self.cap:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: Nie mozna odtworzyc.")
            return

        self.start_playing()

    def start_playing(self):
        if not self.playing:
            self.playing = True
            self.timer.start(33)

    def stop_playing(self):
        if self.playing:
            self.playing = False
            self.timer.stop()

    def restart_playing(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.start_playing()

    def next_frame(self):
        if self.cap and not self.playing:
            ret, frame = self.cap.read()
            if ret:
                self.update_view_with_frame(frame)

    def prev_frame(self):
        if self.cap and not self.playing:
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            if current_frame > 1:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 2)
                ret, frame = self.cap.read()
                if ret:
                    self.update_view_with_frame(frame)

    def refresh_frame(self):
        if self.cap:
            if not self.playing:
                ret, frame = self.cap.read()
                if ret:
                    self.update_frame()

    def update_view_with_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def update_frame(self):
        if self.playing and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.update_view_with_frame(frame)
            else:
                self.stop_playing()