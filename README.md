## Dynamic Population Simulation

This project simulates two phenomena on a directed graph:

Cascade effects (e.g., information spread)

COVID-19 propagation using an SIRS model

The simulation uses a .gml network file to model how information or disease propagates through a population under various conditions.

# Requirements: 
''' pip install networkx matplotlib '''

# Files: 
dynamic_population.py: Main script to run the simulation
cascadebehavior.gml : Sample network graph in GML format

# How to Run: 
Navigate to the folder containing the files and run: 
''' 
python dynamic_population.py <graph_file> --action [cascade|covid] [options]
'''

# Casade Example: 
'''
python dynamic_population.py cascadebehaviour.gml \
  --action cascade \
  --initiator 1,2,5 \
  --threshold 0.33 \
  --plot
'''

# COVID Example: 
'''
python dynamic_population.py cascadebehaviour.gml \
  --action covid \
  --initiator 3,4 \
  --probability_of_infection 0.02 \
  --lifespan 100 \
  --shelter 0.3 \
  --vaccinations 0.24 \
  --plot
  '''
