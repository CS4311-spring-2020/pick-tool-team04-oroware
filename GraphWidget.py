from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

from Icon import Icon
from LogEntry import LogEntry

class GraphWidget(QWidget):

    MINIMUM_NODE_SIZE = 1000
    STARTING_NODE_SIZE = 2000
    MAXIMUM_NODE_SIZE = 5000
    MINIMUM_ICON_SIZE = 0.07
    STARTING_ICON_SIZE = 0.1
    MAXIMUM_ICON_SIZE = 0.15
    MINIMUM_FONT_SIZE = 10
    STARTING_FONT_SIZE = 12
    MAXIMUM_FONT_SIZE = 20

    def __init__(self, parent, trigger, mutable=True):
        self.trigger = trigger
        super(GraphWidget, self).__init__(parent)
        if mutable:
            self.initUI()
        else:
            self.initImmutableUI()

    def initUI(self):
        self.setGeometry(10, 10, 505, 476)
        self.vector = None
        self.node1 = None
        self.node2 = None
        self.axis1 = None
        self.axis2 = None
        self.nodeSize = GraphWidget.STARTING_NODE_SIZE
        self.fontSize = GraphWidget.STARTING_FONT_SIZE
        self.iconSize = GraphWidget.STARTING_ICON_SIZE
        self.iconMapping = dict()
        self.axisMapping = dict()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('button_release_event', self.onRelease)
        self.vbox.addWidget(self.canvas)

    def initImmutableUI(self):
        self.setGeometry(10, 10, 505, 476)
        self.vector = None
        self.nodeSize = GraphWidget.STARTING_NODE_SIZE
        self.fontSize = GraphWidget.STARTING_FONT_SIZE
        self.iconSize = GraphWidget.STARTING_ICON_SIZE
        self.iconMapping = dict()
        self.axisMapping = dict()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.vbox.addWidget(self.canvas)

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
            self.nodeLabels[helperNodeCounter] = ""
            helperNodeCounter -= 1
            self.vectorGraph.add_nodes_from([helperNodeCounter])
            self.pos[helperNodeCounter] = (i, 2)
            self.nodeLabels[helperNodeCounter] = ""
            helperNodeCounter -= 1

    def createNodeLabel(self, significantEvent):
        nodeLabel = " ID: " + str(significantEvent.id)
        if self.vector.visibility["Node Name"]:
            nodeLabel += "\n Name: " + significantEvent.name
        if self.vector.visibility["Node Description"]:
            nodeLabel += "\n Description: " + significantEvent.description
        if self.vector.visibility["Artifact"]:
            nodeLabel += "\n Artifact: " + significantEvent.logEntry.artifact
        if self.vector.visibility["Node Timestamp"]:
            nodeLabel += "\n Timestamp: " + significantEvent.logEntry.date
        if self.vector.visibility["Event Creator"]:
            nodeLabel += "\n Creator: " + significantEvent.logEntry.creator
        if self.vector.visibility["Event Type"]:
            nodeLabel += "\n Type: " + significantEvent.logEntry.eventType
        return nodeLabel

    def initializeVector(self, vector):
        self.vectorGraph = nx.DiGraph()
        self.vector = vector
        self.pos = dict()
        self.nodeLabels = dict()
        self.iconLabels = dict()
        self.edgeLabels = dict()
        self.initializeHelperNodes()
        for significantEventId, significantEvent in vector.significantEvents.items():
            if significantEvent.iconType != Icon.DEFAULT:
                self.iconMapping[significantEventId] = significantEvent.icon
                self.iconLabels[significantEventId] = self.createNodeLabel(significantEvent)
                self.nodeLabels[significantEventId] = ""
            else:
                self.nodeLabels[significantEventId] = self.createNodeLabel(significantEvent)
            self.vectorGraph.add_node(significantEventId)
            self.pos[significantEventId] = significantEvent.position
        for relationship in list(vector.relationships.values()):
            self.vectorGraph.add_edges_from([(relationship.sourceSignificantEventId, relationship.destSignificantEventId)])
            self.edgeLabels[(relationship.sourceSignificantEventId, relationship.destSignificantEventId)] = relationship.description

    def onclick(self, event):
        self.node1 = (event.xdata, event.ydata)
        self.axis1 = event.inaxes
        if self.axis1 in self.axisMapping:
            self.node1 = {self.axisMapping[self.axis1] : self.pos[self.axisMapping[self.axis1]]}
            return
        threshold = 0.10
        for key, value in self.vector.significantEvents.items():
            xValueDifference = max(value.position[0], self.node1[0]) - min(value.position[0], self.node1[0])
            yValueDifference = max(value.position[1], self.node1[1]) - min(value.position[1], self.node1[1])
            if xValueDifference <= threshold and yValueDifference <= threshold:
                self.node1 = {key : self.node1}
                break


    def onRelease(self, event):
        self.node2 = (event.xdata, event.ydata)
        self.axis2 = event.inaxes
        threshold = 0.10
        if self.axis2 not in self.axisMapping:
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
        else:
            self.node2 = {self.axisMapping[self.axis2] : self.pos[self.axisMapping[self.axis2]]}
            firstNodeName = list(self.node1.keys())[0]
            secondNodeName = list(self.node2.keys())[0]
            if firstNodeName != secondNodeName:
                self.vectorGraph.add_edges_from([(firstNodeName, secondNodeName)])
                self.vector.addNewRelationship(firstNodeName, secondNodeName)
                self.trigger.emitRelationshipTableTrigger()
        self.axis1 = None
        self.axis2 = None
        self.node1 = None
        self.node2 = None
        self.plotGraph()

    def plotGraph(self):
        self.nodeSizes = list()
        self.nodeColors = list()
        for i in list(self.pos.keys()):
            if i < 0:
                self.nodeColors.append("white")
                self.nodeSizes.append(self.STARTING_NODE_SIZE)
            else:
                if i in self.iconMapping:
                    self.nodeColors.append("white")
                elif self.vector.significantEvents[i].logEntry.creator == LogEntry.WHITE_TEAM:
                    self.nodeColors.append("grey")
                elif self.vector.significantEvents[i].logEntry.creator == LogEntry.BLUE_TEAM:
                    self.nodeColors.append("cyan")
                elif self.vector.significantEvents[i].logEntry.creator == LogEntry.RED_TEAM:
                    self.nodeColors.append("red")
                self.nodeSizes.append(self.nodeSize)
        self.paint()

    def paint(self):
        self.figure.clf()
        nx.draw(self.vectorGraph, node_size=self.nodeSizes, node_color=self.nodeColors, pos=self.pos,
                font_color="black")
        nx.draw_networkx_labels(self.vectorGraph, pos=self.pos, labels=self.nodeLabels, font_size=self.fontSize)
        nx.draw_networkx_edge_labels(self.vectorGraph, pos=self.pos, edge_labels=self.edgeLabels,
                                     font_size=self.fontSize)
        if len(self.iconMapping) > 0:
            ax = plt.gca()
            fig = plt.gcf()
            trans = ax.transData.transform
            trans2 = fig.transFigure.inverted().transform
            iconSize = self.iconSize
            for node in self.vectorGraph:
                if node in self.iconMapping:
                    (x, y) = self.pos[node]
                    xx, yy = trans((x, y))
                    xa, ya = trans2((xx, yy))
                    a = plt.axes([xa - iconSize/2, ya - iconSize/2, iconSize, iconSize])
                    self.axisMapping[a] = node
                    a.imshow(self.iconMapping[node].graphImage)
                    a.text(0, 0, self.iconLabels[node], fontsize=self.fontSize)
                    a.set_aspect('equal')
                    a.axis('off')
            ax.axis('off')
        self.canvas.draw_idle()

    def maximize(self):
        if self.vector:
            self.nodeSize = (self.nodeSize + 300) if self.nodeSize < GraphWidget.MAXIMUM_NODE_SIZE else GraphWidget.MAXIMUM_NODE_SIZE
            self.fontSize = (self.fontSize + 1) if self.fontSize < GraphWidget.MAXIMUM_FONT_SIZE else GraphWidget.MAXIMUM_FONT_SIZE
            self.iconSize = (self.iconSize + 0.01) if self.iconSize < GraphWidget.MAXIMUM_ICON_SIZE else GraphWidget.MAXIMUM_ICON_SIZE
            print
            self.plotGraph()

    def minimize(self):
        if self.vector:
            self.nodeSize = (self.nodeSize - 300) if self.nodeSize > GraphWidget.MINIMUM_NODE_SIZE else GraphWidget.MINIMUM_NODE_SIZE
            self.fontSize = (self.fontSize - 1) if self.fontSize > GraphWidget.MINIMUM_FONT_SIZE else GraphWidget.MINIMUM_FONT_SIZE
            self.iconSize = (self.iconSize - 0.01) if self.iconSize > GraphWidget.MINIMUM_ICON_SIZE else GraphWidget.MINIMUM_ICON_SIZE
            self.plotGraph()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())