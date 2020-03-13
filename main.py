import snap
import csv
import pandas as pd
import os
import numpy as np
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


# Opens the file
def open_file():
    data = pd.read_csv(r'Scotland_2018.csv')
    data = data.round(3)
    return data


def main():
    data = open_file()
    df = process_data(data)
    print(df)
    generate_graph(df)
    print("Complete")


def process_data(data):
    df = pd.DataFrame(data, columns=['road_name', 'local_authority_name'])
    return df


def search_array(name, array):
    i = 0
    while i < len(array):
        if name == array[i]:
            return True
        i+=1
    return False


def generate_graph(df):
    region_array = []
    road_array = []
    G1 = snap.TUNGraph.New()
    for index, row in df.iterrows():
        if not search_array(row['local_authority_name'], region_array):
            region_array.append(row['local_authority_name'])
            G1.AddNode(index)
        if not search_array(row['road_name'], road_array):
            road_array.append(row['road_name'])
    snap.DrawGViz(G1, snap.gvlCirco, "graph.png", "Scotland's Roads", True)


main()
