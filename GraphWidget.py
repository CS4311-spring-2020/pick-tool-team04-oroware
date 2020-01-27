from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import netgraph

class GraphWidget(QWidget):

    def __init__(self, parent):
        super(GraphWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 10, 505, 476)
        self.center()
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('button_release_event', self.onRelease)
        self.vector = nx.DiGraph()
        self.pos = dict()
        self.node1 = None
        self.node2 = None
        self.vector.add_nodes_from([1, 2, 3, 4], bipartite=0)
        self.vector.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        self.vector.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])
        xValues = set(n for n, d in self.vector.nodes(data=True) if d['bipartite'] == 0)
        yValues = set(self.vector) - xValues
        xValues = sorted(xValues, reverse=True)
        yValues = sorted(yValues, reverse=True)
        self.pos.update((n, (1, i)) for i, n in enumerate(xValues)) # put nodes from X at x=1
        self.pos.update((n, (2, i)) for i, n in enumerate(yValues)) # put nodes from Y at x=2
        vbox.addWidget(self.canvas)
        self.plotGraph()
        self.show()

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
        elif type(self.node2) is dict and type(self.node1) is dict:
            firstNodeName = list(self.node1.keys())[0]
            secondNodeName = list(self.node2.keys())[0]
            self.vector.add_edges_from([(firstNodeName, secondNodeName)])
        else:
            pass
        self.node1 = None
        self.node2 = None
        self.plotGraph()

    def plotGraph(self):
        self.figure.clf()
        nx.draw(self.vector, pos=self.pos, with_labels=True)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())