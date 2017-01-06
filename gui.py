import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt
from trans_media import SignalCarrier as sc
from grid import Grid
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QLabel, QPushButton)
import random
import string
import time


def _translate(context, text, disambig):
    return QApplication.translate(context, text, disambig)


class ui_simulator(object):
    def init_ui(self, simulator):
        simulator.setObjectName("Simulator")
        simulator.setFixedSize(748, 519)
        self.frame = QFrame(simulator)
        self.frame.setGeometry(QtCore.QRect(50, 340, 651, 151))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.group = QGroupBox(self.frame)
        self.group.setGeometry(QtCore.QRect(10, 10, 171, 131))
        self.group.setObjectName("group")
        self.rb_1 = QRadioButton(self.group)
        self.rb_1.setGeometry(QtCore.QRect(10, 30, 82, 17))
        self.rb_1.setObjectName("rb")
        self.rb_1.toggled.connect(lambda: self.show_nodes(self.rb_1))
        self.rb_2 = QRadioButton(self.group)
        self.rb_2.setGeometry(QtCore.QRect(10, 50, 82, 17))
        self.rb_2.setObjectName("rb_2")
        self.rb_2.toggled.connect(lambda: self.show_nodes(self.rb_2))
        self.rb_3 = QRadioButton(self.group)
        self.rb_3.setGeometry(QtCore.QRect(10, 70, 82, 17))
        self.rb_3.setObjectName("rb_3")
        self.rb_3.toggled.connect(lambda: self.show_nodes(self.rb_3))
        self.rb_4 = QRadioButton(self.group)
        self.rb_4.setGeometry(QtCore.QRect(10, 90, 82, 17))
        self.rb_4.setObjectName("rb_4")
        self.rb_4.toggled.connect(lambda: self.show_nodes(self.rb_4))
        self.button = QPushButton(self.frame)
        self.button.setGeometry(QtCore.QRect(210, 110, 75, 23))
        self.button.setObjectName("button")
        self.button.clicked.connect(self.runner)
        # self.button.click(self, PyQt5.QtWidgets.PYQT_SIGNAL("clicked()"), self.runner)
        # QObject.connect(self.button, PYQT_SIGNAL("clicked()"), b2_clicked)
        self.button.setToolTip('Run simulation using selected number of nodes')
        self.frame_2 = QFrame(simulator)
        self.frame_2.setGeometry(QtCore.QRect(50, 39, 641, 291))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.graphics = QGraphicsView(self.frame_2)
        self.graphics.setGeometry(QtCore.QRect(0, 0, 641, 291))
        self.graphics.setObjectName("graphics")
        self.scene = QGraphicsScene(0, 0, 600, 250)
        self.label = QLabel(simulator)
        self.label.setGeometry(QtCore.QRect(50, 10, 61, 20))
        self.label.setObjectName("label")
        self.console = QLabel(self.frame)
        self.console.setGeometry(QtCore.QRect(300, 10, 61, 20))
        self.console.setObjectName("console_label")
        self.textarea = QTextEdit(simulator)
        self.textarea.setStyleSheet("color: white; background-color: black;")
        self.textarea.setReadOnly(True)
        self.textarea.setGeometry(QtCore.QRect(410, 350, 300, 131))
        self.textarea.setObjectName("textarea")
        self.retranslate_ui(simulator)
        QtCore.QMetaObject.connectSlotsByName(simulator)

    def retranslate_ui(self, simulator):
        simulator.setWindowTitle(_translate("Simulator", "Simulator", None))
        self.group.setTitle(_translate("Simulator", "Nodes:", None))
        self.console.setText("Console: ")
        self.rb_1.setText(_translate("Simulator", "5", None))
        self.rb_2.setText(_translate("Simulator", "10", None))
        self.rb_3.setText(_translate("Simulator", "15", None))
        self.rb_4.setText(_translate("Simulator", "20", None))
        self.button.setText(_translate("Simulator", "Start", None))
        self.label.setText(_translate("Simulator", "Node Grid:", None))

    @pyqtSlot()
    def runner(self):
        grid = Grid()
        air = sc()
        self.group.setEnabled(False)
        self.textarea.setTextColor(Qt.white)
        node_names = list(string.ascii_uppercase)
        for i in range(len(self.random_x)):
            grid.add_node(node_names[i], self.random_x[i], self.random_y[i])
        # grid.establish_conn()
        grid.establish_conn(True)
        nd = grid.node_dictionary
        # print(nd.keys())
        for n in nd.values():
            # print(str(n.x_pos) + " " +str(n.y_pos))
            self.textarea.append(str(n.name) + " Neighbor Table: "
                                 + str([x.name for x in n.neighbors.keys()])
                                 + "\nRouting table: " + str(n.RT) + "\n")
        for item in self.graphics.scene().items():
            i = self.graphics.scene().items().index(item)
            item.setToolTip("Node name: " + str(node_names[i])
                            + "\n X: " + str(self.random_x[i]) + " Y: " + str(self.random_y[i]))
        for x in range(5):
            for item in self.graphics.scene().items():
                item.setBrush(Qt.green)
            self.textarea.append("Transmission attempt: " + str(x + 1))
            src = nd[random.choice(list(nd.keys()))]
            dst = nd[random.choice(list(nd.keys()))]
            while src is dst:
                dst = nd[random.choice(list(nd.keys()))]
            src.prepare_msg(src, dst, 'Hi')
            self.textarea.append("Sending from " + src.name + " to " + dst.name)
            while src.buffer:
                src_pos = self.random_x.index(src.x_pos)
                dst_pos = self.random_x.index(dst.x_pos)
                self.graphics.scene().items()[src_pos].setBrush(Qt.blue)
                self.graphics.scene().items()[dst_pos].setBrush(Qt.red)
                self.textarea.append("Current Transmission range (" + src.name + "): "
                                     + str(src.t_range) + "m")
                air.carry(src.send_msg())
                rcv = list(air.transmit_to)
                self.textarea.append("Next hop: " + str(air.message.target_node))
                air.propagate(self.textarea)
                for node in rcv:
                    if node.buffer:
                        src = node
                QApplication.processEvents()
                time.sleep(0.5)
            self.textarea.append('-------------')
        self.group.setEnabled(True)

    def show_nodes(self, button):
        self.scene.setSceneRect(0, 0, 600, 250)
        self.textarea.setText("")
        self.scene.clear()
        # scene.setSceneRect(0, 0, 600, 250)
        nodes = int(button.text())
        self.random_x = random.sample(range(1, 31), nodes)
        self.random_y = random.sample(range(1, 31), nodes)
        for i in range(len(self.random_x)):
            item = QGraphicsEllipseItem(self.random_x[i] * 8, self.random_y[i] * 8, 15, 15)
            item.setToolTip("X: " + str(self.random_x[i]) + " Y: " + str(self.random_y[i]))
            item.setBrush(Qt.green)
            self.scene.addItem(item)
        self.graphics.setScene(self.scene)
        self.graphics.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    simulator = QDialog()
    ui = ui_simulator()
    ui.init_ui(simulator)
    simulator.show()
    sys.exit(app.exec_())
