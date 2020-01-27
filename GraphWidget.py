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
        self.vector = nx.Graph()
        self.pos = dict()
        self.node1 = None
        self.node2 = None
        self.vector.add_nodes_from([1, 2, 3, 4], bipartite=0)
        self.vector.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        self.vector.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])
        x_values = set(n for n, d in self.vector.nodes(data=True) if d['bipartite'] == 0)
        y_values = set(self.vector) - x_values
        x_values = sorted(x_values, reverse=True)
        y_values = sorted(y_values, reverse=True)
        self.pos.update((n, (1, i)) for i, n in enumerate(x_values)) # put nodes from X at x=1
        self.pos.update((n, (2, i)) for i, n in enumerate(y_values)) # put nodes from Y at x=2
        vbox.addWidget(self.canvas)
        self.plotGraph()
        self.show()

    def onclick(self, event):
        self.node1 = (event.xdata, event.ydata)
        threshold = 0.03
        for key, value in self.pos.items():
            x_value_difference = max(value[0], self.node1[0]) - min(value[0], self.node1[0])
            y_value_difference = max(value[1], self.node1[1]) - min(value[1], self.node1[1])
            if x_value_difference <= threshold and y_value_difference <= threshold:
                self.node1 = {key : self.node1}
                break

    def onRelease(self, event):
        self.node2 = (event.xdata, event.ydata)
        threshold = 0.03
        for key, value in self.pos.items():
            x_value_difference = max(value[0], self.node2[0]) - min(value[0], self.node2[0])
            y_value_difference = max(value[1], self.node2[1]) - min(value[1], self.node2[1])
            if x_value_difference <= threshold and y_value_difference <= threshold:
                self.node2 = {key: self.node1}
                break
        if type(self.node2) is not dict and type(self.node1) is dict:
            node_name = list(self.node1.keys())[0]
            self.pos[node_name] = (event.xdata, event.ydata)
        elif type(self.node2) is dict and type(self.node1) is dict:
            first_node_name = list(self.node1.keys())[0]
            second_node_name = list(self.node2.keys())[0]
            self.vector.add_edges_from([(first_node_name, second_node_name)])
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