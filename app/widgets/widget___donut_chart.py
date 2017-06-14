import random

from PyQt4.QtGui import *


class DonutChartWidget(QWidget):
    def __init__(self):
        super(DonutChartWidget, self).__init__()

        scene = QGraphicsScene(self)
        self.grid = QGridLayout(self)

        families = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        total = 0
        set_angle = 0
        count1 = 0
        colours = []
        total = sum(families)

        for count in range(len(families)):
            number = []
            for count in range(3):
                number.append(random.randrange(0, 255))
            colours.append(QColor(number[0], number[1], number[2]))

        for family in families:
            # Max span is 5760, so we have to calculate corresponding span angle
            angle = round(float(family * 5760) / total)
            ellipse = QGraphicsEllipseItem(0, 0, 400, 400)
            ellipse.setPos(0, 0)
            ellipse.setStartAngle(set_angle)
            ellipse.setSpanAngle(angle)
            ellipse.setBrush(colours[count1])
            set_angle += angle
            count1 += 1
            scene.addItem(ellipse)

        view = QGraphicsView(scene)
        self.grid.addWidget(view)
        view.show()
