#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division



__author__ = "Jonathan Grimm"
__date__ = "created: 12.06.18 converted to 3.8: 05.2020"
__IDE__ = "PyCharm Community Edition"

import math
from PlanetSpaceObject import SpaceObject
from PlanetVector import Vector
from PlanetCalculation import Calculations
from PyQt5 import QtGui, QtWidgets,QtCore
import time
import threading
import numpy as np
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, universe):
        super(MainWindow, self).__init__()
        self.canvas = Canvas(universe)
        self.setCentralWidget(self.canvas)
        self.setWindowTitle("Planetensimulation")
        self.setGeometry(0, 0, 1300, 1300)
        self.show()

        self.calc = Calculations(universe, settings)

    def closeEvent(self, event):
        self.canvas.runtime = False
        self.calc.runtime = False

class Canvas(QtWidgets.QWidget):
    def __init__(self, universe):
        super(Canvas, self).__init__()
        self.qp = QtGui.QPainter()
        self.setGeometry(300, 300, 1200, 1200)
        self.setWindowTitle("PlanetSimulation")

        self.universe = universe
        self.cb_trajectory = QtWidgets.QCheckBox("Trajectory", self)
        self.cb_trajectory.setChecked(settings.trajectory)
        self.cb_trajectory.stateChanged.connect(self.set_trajetory)
        self.cb_trajectory.move(470, 12)

        # planetozentisch
        self.cb_geo = QtWidgets.QCheckBox("Heliocentric", self)
        self.cb_geo.move(550, 12)
        self.cb_geo.setChecked(settings.heliocentric)
        self.cb_geo.stateChanged.connect(self.heliocentric_changed)
        self.cb_geo.setEnabled(False)

        #showing fps
        self.l = QtWidgets.QLabel("0 fps", self)
        self.l.setGeometry(10, 10, 150, 36)
        self.lastTime = time.time()
        self.fps = None

        # Focus
        self.l_focus = QtWidgets.QLabel("Focus:", self)
        self.l_focus.setGeometry(650, 10,750,20)
        self.cobo_focus = QtWidgets.QComboBox(self)
        self.cobo_focus.addItem(settings.standart_focus.name)
        for p in self.universe:
            self.cobo_focus.addItem(p.name)
        self.cobo_focus.move(700, 10)
        self.cobo_focus.currentIndexChanged.connect(self.focus_chanege)
        cbtexts = [self.cobo_focus.itemText(i) for i in range(self.cobo_focus.count())]
        self.cobo_focus.setCurrentIndex(cbtexts.index(settings.focus.name))


        self.runtime = True
        t = threading.Thread(target=self.myupdate)
        t.start()

    def heliocentric_changed(self, i):
        if i == 2:
            settings.heliocentric = True
        else:
            settings.heliocentric = False

        # deletes trajectories for previous centrism
        for planet in self.universe:
            planet.trajectory = []
            planet.trajectory2 = []

    def focus_chanege(self, i):
        if i == 0:
            settings.focus = settings.standart_focus
        else:
            settings.focus = self.universe[i - 1]
        for planet in self.universe:
            planet.trajectory = []
            planet.trajectory2 = []

    def set_trajetory(self):
        if settings.trajectory:
            self.cb_geo.setEnabled(False)
            settings.trajectory = False
            for planet in self.universe:
                planet.trajectory = []
                planet.trajectory2 = []  # np.array([])
        else:
            settings.trajectory = True
            self.cb_geo.setEnabled(True)

    def myupdate(self):
        while self.runtime:
            self.update()
            # QtTest.QTest.qWait(10)
            # QtGui.QApplication.processEvents()
            time.sleep(0.001)

            # QtGui.QApplication.processEvents()

    def paintEvent(self, e):
        global settings
        now = time.time()
        dt = now - self.lastTime
        self.lastTime = now
        if self.fps is None:
            self.fps = 1.0 / dt
        else:
            s = np.clip(dt * 3., 0, 1)
            self.fps = self.fps * (1 - s) + (1.0 / dt) * s
        self.l.setText(str(self.fps))

        self.qp.begin(self)

        self.qp.drawRect(0, 0, 1200, 1200)

        for planet in self.universe:
            r, g, b = planet.colour
            self.qp.setBrush(QtGui.QColor(r, g, b))
            self.qp.setPen(0)
            # x = (planet.x - settings.focus.x) * settings.proportion_scaling + settings.scaling[0]-planet.radius/2
            # y = (planet.y - settings.focus.y) * settings.proportion_scaling + settings.scaling[1]-planet.radius/2
            #print(planet.drawx, planet.drawy, planet.radius, planet.radius)
            print(""), #no idea why it crashes when its not there
            #print(type(planet.drawx), type(planet.drawy), type(planet.radius), type(planet.radius))
            self.qp.drawEllipse(planet.drawx, planet.drawy, planet.radius, planet.radius)

            # Trajectory

            if settings.trajectory and len(planet.trajectory2) > 1:
                # print planet.name
                self.qp.setPen(QtGui.QColor(r, g, b))
                # self.qp.drawPolyline(*traj_points)
                try:
                    self.qp.drawPolyline(*planet.trajectory2)
                except TypeError:
                    print("TypeError")
                    pass

        # self.qp.setBrush(QtGui.QColor(255, 0, 0))
        # for i in self.universe:
        #    self.qp.drawEllipse(400 + i.x, 400 + i.y, i.r, i.r)

        self.qp.end()


class Settings:
    def __init__(self):
        (self.width, self.height) = (1200, 1200)
        self.scaling = (int(self.width / 2), int(self.height / 2))
        self.standart_focus = SpaceObject("standart", 0, 0, None, None, None, None)
        self.focus = self.standart_focus
        self.heliocentric = False  # True zeigt heliozentrische Trajektorie
        self.trajectory = False  # zeigt trajektorie an oder nicht
        self.traj_length = 1000

        self.time_scale = 10000000  # wie schnell/langsam alles geht
        # self.time_scale = 31536000 #a year in seconds

        self.proportion_scaling = 1.0 / math.pow(10, 9)  # proportion scaling


settings = Settings()
universe = []
sun = SpaceObject("sun", 0, 0, 1.984 * math.pow(10, 30), Vector(), 50, (225, 225, 0))
universe.append(sun)

earth = SpaceObject("earth", 152.0 * math.pow(10, 9), 0, 5.974 * math.pow(10, 24), Vector(0, -1, 29290), 15,
                    (0, 0, 255))
universe.append(earth)

#moon = SpaceObject("moon",x=152.0 * math.pow(10, 9)+405500,y=0,mass=7.349*math.pow(10,22),velocityVector=Vector(0,1,964),radius=5,colour=(225,225,0))
#universe.append(moon)
venus = SpaceObject("venus", x=108.9 * math.pow(10, 9), y=0, mass=4.869 * math.pow(10, 24),
                    velocityVector=Vector(0, 1, 35020), radius=15, colour=(255, 0, 255))
universe.append(venus)

mars = SpaceObject("mars", x=249 * math.pow(10, 9), y=0, mass=6.419 * math.pow(10, 23),
                   velocityVector=Vector(0, -1, 21970), radius=10, colour=(200, 0, 0))
universe.append(mars)

settings.focus = universe[1]

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    #app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(universe)
    sys.exit(app.exec_())
