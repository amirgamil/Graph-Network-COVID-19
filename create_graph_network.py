import pandas as pd
import numpy as np
import os
import itertools
import json
import plotly.graph_objects as go
import networkx as nx
import networkx.drawing
import matplotlib.pyplot as plt
import pygraphviz as pgv

#load the json data
with open("data.json") as f:
    data = json.load(f)

def parse_json_data(data):
    number_patients = 0
    #This will be an array of arrays representing all of the different adjacent nodes a node will connect to
    #For example if patient 2 was infected by patient 1 and they themselves infected 3,4 - array would be [2,3,4]
    connecting_adjacent_nodes = []
    dict_of_ids_and_nodes={}
    for patient in data:
        number_patients += 1
        temp_array = patient["infecteeIds"]
        if patient["infectorId"] != None:
            temp_array.append(patient["infectorId"])
        #check array is not empty before appending it
        if len(temp_array) > 0:
            connecting_adjacent_nodes.append(temp_array)
        #create dictionary with ids as the keys and all of the nodes to connect to as the values
        dict_of_ids_and_nodes[patient["id"]] = temp_array
    return number_patients, dict_of_ids_and_nodes

num_nodes, nodes_to_connect_to = parse_json_data(data)

#function to format the data into the list of tuples that the graph accepts
def format_nodes_edges_data(connected_nodes):
    list_of_tuples = []
    for (id, nodes) in connected_nodes.items():
        print(nodes)
        for node in nodes:
            list_of_tuples.append((id, node))
    return list_of_tuples
list_of_node_connections = format_nodes_edges_data(nodes_to_connect_to)

#create the graph
G=pgv.AGraph()
#pass in node connections
G.add_edges_from(list_of_node_connections)
G.graph_attr['label']=''
G.node_attr['shape']='circle'
G.edge_attr['color']='red'
G.layout()
G.write("file.dot")
G.draw("file.png")
G=pgv.AGraph("file.dot")
#
# edge_trace = go.Scatter(
#     x=edge_x, y=edge_y,
#     line=dict(width=0.5, color='#888'),
#     hoverinfo='none',
#     mode='lines')
#
# node_x = []
# node_y = []
# for node in G.nodes():
#     x, y = G.nodes[node]['pos']
#     node_x.append(x)
#     node_y.append(y)
#
# node_trace = go.Scatter(
#     x=node_x, y=node_y,
#     mode='markers',
#     hoverinfo='text',
#     marker=dict(
#         showscale=True,
#         # colorscale options
#         #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
#         #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
#         #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
#         colorscale='YlGnBu',
#         reversescale=True,
#         color=[],
#         size=10,
#         colorbar=dict(
#             thickness=15,
#             title='Node Connections',
#             xanchor='left',
#             titleside='right'
#         ),
#         line_width=2))
# node_adjacencies = []
# node_text = []
# for node, adjacencies in enumerate(G.adjacency()):
#     node_adjacencies.append(len(adjacencies[1]))
#     node_text.append('# of connections: '+str(len(adjacencies[1])))
#
# node_trace.marker.color = node_adjacencies
# node_trace.text = node_text
#
# fig = go.Figure(data=[edge_trace, node_trace],
#              layout=go.Layout(
#                 title='<br>Network graph made with Python',
#                 titlefont_size=16,
#                 showlegend=False,
#                 hovermode='closest',
#                 margin=dict(b=20,l=5,r=5,t=40),
#                 annotations=[ dict(
#                     text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
#                     showarrow=False,
#                     xref="paper", yref="paper",
#                     x=0.005, y=-0.002 ) ],
#                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#                 )
# fig.show()
