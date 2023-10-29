from PyQt6.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap


class BoundingBoxDrawer(QLabel):
    def __init__(self, parent=None):
        super(BoundingBoxDrawer, self).__init__(parent)
        self.begin = QPoint()
        self.end = QPoint()
        self.setMouseTracking(True)  # Włącza śledzenie myszy bez konieczności wciskania przycisku.
        self.painted = False  # Flaga wskazująca, czy bounding box został narysowany.

    def mousePressEvent(self, event):
        # Zaczynamy rysowanie bounding boxa.
        if event.button() == Qt.MouseButton.LeftButton:
            self.begin = event.position().toPoint()
            self.end = self.begin
            self.painted = False
            self.update()

    def mouseMoveEvent(self, event):
        # Aktualizujemy końcowy punkt naszego boxa i przerysowujemy.
        if not self.begin.isNull() and not self.painted:
            self.end = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        # Kończymy rysowanie bounding boxa.
        if event.button() == Qt.MouseButton.LeftButton and not self.begin.isNull():
            self.end = event.position().toPoint()
            self.painted = True
            self.update()

            # Emitowanie sygnału lub innego powiadomienia, że bounding box został utworzony, może się odbyć tutaj.

    def paintEvent(self, event):
        # Rysowanie bounding boxa na etykiecie.
        super(BoundingBoxDrawer, self).paintEvent(event)
        if not self.begin.isNull() and not self.end.isNull():
            rect = QRect(self.begin, self.end).normalized()
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine))  # Czerwony prostokąt o grubości 2 piksele.
            painter.drawRect(rect)

    def clear(self):
        # Metoda do czyszczenia bounding boxa (na przykład po zakończeniu przetwarzania klatki).
        self.begin = QPoint()
        self.end = QPoint()
        self.painted = False
        self.update()


# Przykład użycia
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Dodajemy BoundingBoxDrawer.
    box_drawer = BoundingBoxDrawer()
    box_drawer.setPixmap(QPixmap("test_image.jpg"))  # Załaduj przykładowy obraz.
    box_drawer.setFixedSize(QSize(640, 480))  # Ustaw stały rozmiar, aby pasował do Twojego materiału wideo.

    layout.addWidget(box_drawer)

    widget.show()
    sys.exit(app.exec())