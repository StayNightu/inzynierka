import pandas as pd
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout


class Csv_file(QWidget):
    def __init__(self, csv_file_path='./1.csv'):
        super().__init__()
        self.csv_file_path = csv_file_path
        self.text_browser = QTextBrowser()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_browser)
        self.setLayout(self.layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.csv_display)
        self.timer.start(1000)

        self.csv_display()

    def append_to_csv(self, bbox_id):
        try:
            # Wczytywanie obecnych danych, jeśli istnieją
            if pd.io.common.file_exists(self.csv_file_path):
                df = pd.read_csv(self.csv_file_path)
            else:
                df = pd.DataFrame(columns=['ID'])

            # Dodawanie nowego rekordu
            df = df.append({'ID': bbox_id}, ignore_index=True)
            df.to_csv(self.csv_file_path, index=False)

            print(f"Added ID {bbox_id} to CSV.")
            self.csv_display()  # refresh display after writing
        except Exception as e:
            self.text_browser.setPlainText(f"Blad zapisu: {e}")
            print(f"Error appending to CSV: {e}")

    def csv_display(self):
        print("Refreshing CSV display...")  # Wydruk do konsoli
        try:
            df = pd.read_csv(self.csv_file_path)
            data = df.to_string(index=False)
            self.text_browser.setPlainText(data)
        except FileNotFoundError:
            self.text_browser.setPlainText(f"Nie znaleziono: {self.csv_file_path}")
        except Exception as e:
            self.text_browser.setPlainText(f"Blad: {e}")


