import csv
from PyQt6.QtWidgets import *


class Csv_file(QWidget):
    def __init__(self):
        super().__init__()
        self.text_browser = QTextBrowser()
        self.csv_display()

    def csv_display(self):
        csv_file_path = './1.csv'
        try:
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                data = ""
                for row in reader:
                    data += ";".join(row) + "\n"
                self.text_browser.setPlainText(data)

        except FileNotFoundError:
            self.text_browser.setPlainText(f"Nie znaleziono: {csv_file_path}")
        except Exception as e:
            self.text_browser.setPlainText(f"Blad: {e}")

