import numpy as np
from collections import *
import netgraph

# Graph data
G = {'y1': OrderedDict([('y2', OrderedDict([('weight', 0.8688325076457851)])), (1, OrderedDict([('weight', 0.13116749235421485)]))]), 'y2': OrderedDict([('y3', OrderedDict([('weight', 0.29660515972204304)])), ('y4', OrderedDict([('weight', 0.703394840277957)]))]), 'y3': OrderedDict([(4, OrderedDict([('weight', 0.2858185316736193)])), ('y5', OrderedDict([('weight', 0.7141814683263807)]))]), 4: OrderedDict(), 'input': OrderedDict([('y1', OrderedDict([('weight', 1.0)]))]), 'y4': OrderedDict([(3, OrderedDict([('weight', 0.27847763084646443)])), (5, OrderedDict([('weight', 0.7215223691535356)]))]), 3: OrderedDict(), 5: OrderedDict(), 'y5': OrderedDict([(6, OrderedDict([('weight', 0.5733512797415756)])), (2, OrderedDict([('weight', 0.4266487202584244)]))]), 6: OrderedDict(), 1: OrderedDict(), 2: OrderedDict()}
G = nx.from_dict_of_dicts(G)
G_scaffold = {'input': OrderedDict([('y1', OrderedDict())]), 'y1': OrderedDict([('y2', OrderedDict()), (1, OrderedDict())]), 'y2': OrderedDict([('y3', OrderedDict()), ('y4', OrderedDict())]), 1: OrderedDict(), 'y3': OrderedDict([(4, OrderedDict()), ('y5', OrderedDict())]), 'y4': OrderedDict([(3, OrderedDict()), (5, OrderedDict())]), 4: OrderedDict(), 'y5': OrderedDict([(6, OrderedDict()), (2, OrderedDict())]), 3: OrderedDict(), 5: OrderedDict(), 6: OrderedDict(), 2: OrderedDict()}
G_scaffold = nx.from_dict_of_dicts(G_scaffold)
G_sem = {'y1': OrderedDict([('y2', OrderedDict([('weight', 0.046032370518141796)])), (1, OrderedDict([('weight', 0.046032370518141796)]))]), 'y2': OrderedDict([('y3', OrderedDict([('weight', 0.08764771571290508)])), ('y4', OrderedDict([('weight', 0.08764771571290508)]))]), 'y3': OrderedDict([(4, OrderedDict([('weight', 0.06045928834718992)])), ('y5', OrderedDict([('weight', 0.06045928834718992)]))]), 4: OrderedDict(), 'input': OrderedDict([('y1', OrderedDict([('weight', 0.0)]))]), 'y4': OrderedDict([(3, OrderedDict([('weight', 0.12254141747735424)])), (5, OrderedDict([('weight', 0.12254141747735425)]))]), 3: OrderedDict(), 5: OrderedDict(), 'y5': OrderedDict([(6, OrderedDict([('weight', 0.11700701511079069)])), (2, OrderedDict([('weight', 0.11700701511079069)]))]), 6: OrderedDict(), 1: OrderedDict(), 2: OrderedDict()}
G_sem = nx.from_dict_of_dicts(G_sem)

# Edge info
edge_input = ('input', 'y1')
weights_sem = np.array([G_sem[u][v]['weight']for u,v in G_sem.edges()]) * 256

# Layout
pos = nx.nx_agraph.graphviz_layout(G_scaffold, prog="dot", root="input")

# Plotting graph
pad = 10
with plt.style.context("ggplot"):
     fig, ax = plt.subplots(figsize=(8,8))
