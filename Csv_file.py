import csv
from PyQt6.QtWidgets import *


class Csv_file(QWidget):
    def __init__(self):
        super().__init__()
        self.text_browser = QTextBrowser()

    def csv_file(self):
        csv_file_path = './1.csv'
        try:
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                data = ""
                for row in reader:
                    data += ";".join(row) + "\n"
                self.text_browser.setPlainText(data)

        except FileNotFoundError:
            self.text_browser.setPlainText(print(f"Nie znaleziono: {csv_file_path}"))
        except Exception as e:
            self.text_browser.setPlainText(print(f"Blad: {e=}"))

