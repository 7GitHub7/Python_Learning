from PyQt5 import QtWidgets, QtGui, QtCore
import math


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.chosen_points = []

        # tworzenie pixmap
        self.label_pixmap = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(600, 600)
     
        self.label_pixmap.setPixmap(self.pixmap)
        self.label_pixmap.setStyleSheet("border: 1px solid white;")

        # tworzenie przyciskow i przypisywanie do nich funkcji
        self.btn_connect = QtWidgets.QPushButton("Polacz punkty")
        self.btn_connect.clicked.connect(self.connect_points)

        self.btn_sum_sides = QtWidgets.QPushButton("Oblicz obwod")
        self.btn_sum_sides.clicked.connect(self.sum_sides_len)
        self.btn_sum_sides.setDisabled(True)

        self.btn_clean = QtWidgets.QPushButton("Wyczysc")
        self.btn_clean.clicked.connect(self.clean_pixmap)
        self.btn_clean.setDisabled(True)

        self.result_field = QtWidgets.QLabel()
        self.result_field.setMaximumSize(QtCore.QSize(100,50))

        # panel boczny (podział 'wierszami')
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.btn_connect)
        v_box.addWidget(self.btn_clean)
        v_box.addWidget(self.btn_sum_sides)
        v_box.addWidget(self.result_field)

        # kontener główny(podział na 'kolumny')
        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addWidget(self.label_pixmap)

        main_view = QtWidgets.QWidget()
        main_view.setLayout(h_box)

        self.setCentralWidget(main_view)

    # event_handler/metoda odziedziczona po klasie Qwidget
    def mouseReleaseEvent(self, cursor_event):
        self.chosen_points.append([cursor_event.x()-130,cursor_event.y()-40])
        painter = QtGui.QPainter(self.label_pixmap.pixmap())
        painter.drawPixmap(self.rect(),self.pixmap)
        pen = QtGui.QPen()
        pen.setWidth(6)
        pen.setColor(QtGui.QColor("orange"))
        painter.setPen(pen)
        painter.begin
        for pos in self.chosen_points:
            painter.drawPoint(pos[0],pos[1])
        painter.end()
        self.update()

    # łączenie punktów metodą drawLine    
    def connect_points(self):
        print("Polacz")
        if (len(self.chosen_points) > 2):
            painter = QtGui.QPainter(self.label_pixmap.pixmap())
            pen = QtGui.QPen(QtGui.QColor("orange"))
            pen.setWidth(8)
            painter.setPen(pen)
            for point in range(len(self.chosen_points[:-1])):
                painter.drawLine(self.chosen_points[point][0], self.chosen_points[point][1],self.chosen_points[point+1][0], self.chosen_points[point+1][1])
            painter.drawLine(self.chosen_points[0][0], self.chosen_points[0][1], self.chosen_points[-1][0], self.chosen_points[-1][1])
            painter.end()
            self.update()
            self.btn_clean.setDisabled(False)
            self.btn_sum_sides.setDisabled(False)    

    # czyszczenie ekranu poprzez wypełnienie pixmapy domyślnym kolorem
    def clean_pixmap(self):
        self.label_pixmap.pixmap().fill(QtGui.QColor('black'))
        self.result_field.clear()
        self.chosen_points.clear()
        self.btn_clean.setDisabled(True)
        self.btn_sum_sides.setDisabled(True)
        self.update()         
    
    # oblicznie odległosci miedzy punktami metodą Euklidesa
    def sum_sides_len(self):
        total_length = 0
        for point in range(len(self.chosen_points[:-1])):
            p = [self.chosen_points[point][0],self.chosen_points[point][0]]
            q = [self.chosen_points[point][1],self.chosen_points[point+1][1]]
            total_length += math.dist(p,q)
        total_length += math.dist(p,q)        
        self.result_field.setText(f'Obwod :\n {round(total_length,2)}')
       

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())







