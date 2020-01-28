from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

class GraphWidget(QWidget):

    def __init__(self, parent, trigger):
        self.trigger = trigger
        super(GraphWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 10, 505, 476)
        self.center()
        self.vector = None
        self.vectorGraph = nx.DiGraph()
        self.node1 = None
        self.node2 = None
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('button_release_event', self.onRelease)
        vbox.addWidget(self.canvas)

    def draw(self):
        self.plotGraph()
        self.show()

    def initializeVector(self, vector):
        self.vector = vector
        self.pos = dict()
        for significantEventId, significantEvent in vector.significantEvents.items():
            self.vectorGraph.add_node(significantEventId)
            self.pos[significantEventId] = significantEvent.position
        for relationship in list(vector.relationships.values()):
            self.vectorGraph.add_edges_from([relationship.sourceSignificantEventId, relationship.destSignificantEventId])

    def onclick(self, event):
        self.node1 = (event.xdata, event.ydata)
        threshold = 0.03
        for key, value in self.pos.items():
            xValueDifference = max(value[0], self.node1[0]) - min(value[0], self.node1[0])
            yValueDifference = max(value[1], self.node1[1]) - min(value[1], self.node1[1])
            if xValueDifference <= threshold and yValueDifference <= threshold:
                self.node1 = {key : self.node1}
                break

    def onRelease(self, event):
        self.node2 = (event.xdata, event.ydata)
        threshold = 0.03
        for key, value in self.pos.items():
            xValue_difference = max(value[0], self.node2[0]) - min(value[0], self.node2[0])
            yValue_difference = max(value[1], self.node2[1]) - min(value[1], self.node2[1])
            if xValue_difference <= threshold and yValue_difference <= threshold:
                self.node2 = {key: self.node1}
                break
        if type(self.node2) is not dict and type(self.node1) is dict:
            node_name = list(self.node1.keys())[0]
            self.pos[node_name] = (event.xdata, event.ydata)
            self.vector.significantEvents[node_name].position = (event.xdata, event.ydata)
        elif type(self.node2) is dict and type(self.node1) is dict:
            firstNodeName = list(self.node1.keys())[0]
            secondNodeName = list(self.node2.keys())[0]
            self.vectorGraph.add_edges_from([(firstNodeName, secondNodeName)])
            self.vector.addNewRelationship(firstNodeName, secondNodeName)
            self.trigger.emit_trigger()
        else:
            pass
        self.node1 = None
        self.node2 = None
        self.plotGraph()

    def plotGraph(self):
        self.figure.clf()
        nx.draw(self.vectorGraph, pos=self.pos, with_labels=True)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())