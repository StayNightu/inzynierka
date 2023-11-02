from PyQt6.QtWidgets import QLabel, QInputDialog
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt, QPoint
class BoundingBoxDrawer(QLabel):
    def __init__(self, csv_writer=None):
        super().__init__()
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.drawing = False
        self.bboxes = []
        self.currentID = 1
        self.csv_writer = csv_writer


    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        if self.drawing:
            painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.PenStyle.SolidLine))
            painter.drawRect(self.startPoint.x(), self.startPoint.y(), self.endPoint.x() - self.startPoint.x(),
                             self.endPoint.y() - self.startPoint.y())
            painter.setFont(QFont("Arial", 10))
            painter.drawText(self.startPoint, f"ID: {self.currentID}")

        for bbox in self.bboxes:
            start = bbox["start"]
            end = bbox["end"]
            id = bbox["id"]
            painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.PenStyle.SolidLine))
            painter.drawRect(start.x(), start.y(), end.x() - start.x(), end.y() - start.y())
            painter.setFont(QFont("Arial", 10))
            painter.drawText(start, f"ID: {id}")

    def mousePressEvent(self, event):
        self.drawing = True
        self.startPoint = event.position().toPoint()
        self.endPoint = self.startPoint
        self.update()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.endPoint = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False
        if self.startPoint != self.endPoint:
            self.bboxes.append({"start": self.startPoint, "end": self.endPoint, "id": self.currentID})
            if self.csv_writer:
                self.csv_writer.append_to_csv(self.currentID)
            self.currentID += 1
        self.update()

    def add_bbox(self):
        self.drawing = True

    def edit_bbox(self):
        if self.bboxes:
            new_id, ok = QInputDialog.getInt(self, "Edit BBox", "Enter new ID:", self.bboxes[-1]["id"], 1, 1000, 1)
            if ok:
                self.bboxes[-1]["id"] = new_id

    def delete_bbox(self):
        if self.bboxes:
            self.bboxes.pop()