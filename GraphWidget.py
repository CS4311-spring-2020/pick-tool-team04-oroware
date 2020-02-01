from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

from LogEntry import LogEntry


class GraphWidget(QWidget):

    MINIMUM_NODE_SIZE = 1000
    STARTING_NODE_SIZE = 2000
    MAXIMIMUM_NODE_SIZE = 5000
    def __init__(self, parent, trigger):
        self.trigger = trigger
        super(GraphWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 10, 505, 476)
        self.vector = None
        self.node1 = None
        self.node2 = None
        self.nodeSize = GraphWidget.STARTING_NODE_SIZE
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

    def export(self):
        if self.vector != None:
           self.figure.savefig((self.vector.vectorName + "_Graph.png"), format="PNG")

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
                self.trigger.emitRelationshipTableTrigger()
        else:
            pass
        self.node1 = None
        self.node2 = None
        self.plotGraph()

    def plotGraph(self):
        self.figure.clf()
        nodeSizes = list()
        nodeColors = list()
        for i in list(self.pos.keys()):
            if i < 0:
                nodeColors.append("white")
                nodeSizes.append(self.STARTING_NODE_SIZE)
            else:
                if self.vector.significantEvents[i].logEntry.creator == LogEntry.WHITE_TEAM:
                    nodeColors.append("grey")
                elif self.vector.significantEvents[i].logEntry.creator == LogEntry.BLUE_TEAM:
                    nodeColors.append("blue")
                elif self.vector.significantEvents[i].logEntry.creator == LogEntry.RED_TEAM:
                    nodeColors.append("maroon")
                nodeSizes.append(self.nodeSize)
        nx.draw(self.vectorGraph, node_size=nodeSizes, node_color=nodeColors, pos=self.pos, with_labels=True, font_color="white")
        self.canvas.draw_idle()

    def maximize(self):
        if self.vector:
            self.figure.clf()
            nodeSizes = list()
            nodeColors = list()
            self.nodeSize = (self.nodeSize + 300) if self.nodeSize < GraphWidget.MAXIMIMUM_NODE_SIZE else GraphWidget.MAXIMIMUM_NODE_SIZE
            for i in list(self.pos.keys()):
                if i < 0:
                    nodeColors.append("white")
                    nodeSizes.append(GraphWidget.STARTING_NODE_SIZE)
                else:
                    if self.vector.significantEvents[i].logEntry.creator == LogEntry.WHITE_TEAM:
                        nodeColors.append("grey")
                    elif self.vector.significantEvents[i].logEntry.creator == LogEntry.BLUE_TEAM:
                        nodeColors.append("blue")
                    elif self.vector.significantEvents[i].logEntry.creator == LogEntry.RED_TEAM:
                        nodeColors.append("maroon")
                    nodeSizes.append(self.nodeSize)
            nx.draw(self.vectorGraph, node_size=nodeSizes, node_color=nodeColors, pos=self.pos, with_labels=True,
                    font_color="white")
            self.canvas.draw_idle()

    def minimize(self):
        if self.vector:
            self.figure.clf()
            nodeSizes = list()
            nodeColors = list()
            self.nodeSize = (self.nodeSize - 300) if self.nodeSize > GraphWidget.MINIMUM_NODE_SIZE else GraphWidget.MINIMUM_NODE_SIZE
            for i in list(self.pos.keys()):
                if i < 0:
                    nodeColors.append("white")
                    nodeSizes.append(GraphWidget.STARTING_NODE_SIZE)
                else:
                    if self.vector.significantEvents[i].logEntry.creator == LogEntry.WHITE_TEAM:
                        nodeColors.append("grey")
                    elif self.vector.significantEvents[i].logEntry.creator == LogEntry.BLUE_TEAM:
                        nodeColors.append("blue")
                    elif self.vector.significantEvents[i].logEntry.creator == LogEntry.RED_TEAM:
                        nodeColors.append("maroon")
                    nodeSizes.append(self.nodeSize)
            nx.draw(self.vectorGraph, node_size=nodeSizes, node_color=nodeColors, pos=self.pos, with_labels=True,
                    font_color="white")
            self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())