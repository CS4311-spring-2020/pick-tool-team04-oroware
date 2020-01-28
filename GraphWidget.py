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
        self.vector = None
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

    def initializeHelperNodes(self):
        helperNodeCounter = -1
        for i in range(self.vector.vectorDimensions):
            self.vectorGraph.add_nodes_from([helperNodeCounter])
            self.pos[helperNodeCounter] = (i, 0)
            helperNodeCounter -= 1
            self.vectorGraph.add_nodes_from([helperNodeCounter])
            self.pos[helperNodeCounter] = (i, 2)
            helperNodeCounter -= 1

    def initializeVector(self, vector):
        self.vectorGraph = nx.DiGraph()
        self.vector = vector
        self.pos = dict()
        self.initializeHelperNodes()
        for significantEventId, significantEvent in vector.significantEvents.items():
            self.vectorGraph.add_nodes_from([significantEventId])
            self.pos[significantEventId] = significantEvent.position
        for relationship in list(vector.relationships.values()):
            self.vectorGraph.add_edges_from([(relationship.sourceSignificantEventId, relationship.destSignificantEventId)])

    def onclick(self, event):
        self.node1 = (event.xdata, event.ydata)
        threshold = 0.10
        for key, value in self.vector.significantEvents.items():
            xValueDifference = max(value.position[0], self.node1[0]) - min(value.position[0], self.node1[0])
            yValueDifference = max(value.position[1], self.node1[1]) - min(value.position[1], self.node1[1])
            if xValueDifference <= threshold and yValueDifference <= threshold:
                self.node1 = {key : self.node1}
                break

    def onRelease(self, event):
        self.node2 = (event.xdata, event.ydata)
        threshold = 0.10
        for key, value in self.vector.significantEvents.items():
            xValueDifference = max(value.position[0], self.node2[0]) - min(value.position[0], self.node2[0])
            yValueDifference = max(value.position[1], self.node2[1]) - min(value.position[1], self.node2[1])
            if xValueDifference <= threshold and yValueDifference <= threshold:
                self.node2 = {key: self.node2}
                break
        if type(self.node2) is not dict and type(self.node1) is dict:
            node_name = list(self.node1.keys())[0]
            self.pos[node_name] = (event.xdata, event.ydata)
            self.vector.significantEvents[node_name].position = (event.xdata, event.ydata)
        elif type(self.node2) is dict and type(self.node1) is dict:
            firstNodeName = list(self.node1.keys())[0]
            secondNodeName = list(self.node2.keys())[0]
            if firstNodeName != secondNodeName:
                self.vectorGraph.add_edges_from([(firstNodeName, secondNodeName)])
                self.vector.addNewRelationship(firstNodeName, secondNodeName)
                self.trigger.emit_trigger()
        else:
            pass
        node_sizes = list()
        for _ in range(len(list(self.pos.keys()))):
            node_sizes.append(2000)
        self.node1 = None
        self.node2 = None
        self.plotGraph()

    def plotGraph(self):
        self.figure.clf()
        node_sizes = list()
        node_colors = list()
        for i in range(len(list(self.pos.keys()))):
            node_sizes.append(2000)
            if i < (2 * self.vector.vectorDimensions):
                node_colors.append("white")
            else:
                node_colors.append("blue")
        nx.draw(self.vectorGraph, node_size=node_sizes, node_color=node_colors, pos=self.pos, with_labels=True, font_color="white")
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())