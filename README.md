# CRC

This repository reproduces all the results reported on our report: "Robustness Analysis of a Terrorist Network"

## Scripts

To generate the image of the graph we created the script: draw_graph.py

To get the overall network structure it can be used the script: overall_network_structure.py

To draw the line charts present in the report we created the scripts: 
draw_line_chart_rm_nodes.py and draw_line_chart_rm_edges.py

The metric used can be changed inside the script by changing the variables: 
get_function and function_string

This scripts generate csv files that can then be used to generate the line charts again with the script:
draw_line_chart_from_csv.py

## Datasets

The dataset used to generate the network was the csv with the weighted connections: indonesianLinksDATASET.csv
There are some nodes that don't have a connection and that are only represented on the dataset: indonesianResultsDATASET.csv