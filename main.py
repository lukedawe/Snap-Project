import snap
import csv
import pandas as pd
import os
import numpy as np
import time

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


# Opens the file
def open_file():
    data = pd.read_csv(r'Scotland_2018.csv', sep=',', error_bad_lines=False, index_col=False, dtype='unicode',
                       low_memory=False)
    data = data.round(3)
    return data


def main():
    start_time = time.time()
    data = open_file()
    df = process_data(data)
    print(df)
    generate_graph(df)
    print("Complete")
    print("--- %s seconds ---" % (time.time() - start_time))


def process_data(data):
    df = pd.DataFrame(data, columns=['road_name', 'local_authority_name'])
    return df


def search_array(name, array):
    i = 0
    while i < len(array):
        if name == array[i]:
            return True
        i += 1
    return False


def generate_graph(df):
    roads_and_regions = {}
    roads_and_regions.setdefault("", [])
    region_array = []
    region_to_index = {}
    G1 = snap.TUNGraph.New()
    label = snap.TIntStrH()
    NIdColourH = snap.TIntStrH()

    for index, row in df.iterrows():

        if not search_array(row['local_authority_name'], region_array):
            region_array.append(row['local_authority_name'])
            region_to_index[row['local_authority_name']] = index
            G1.AddNode(index)
            NIdColourH[index] = "red"
            label[index] = row['local_authority_name']

        if not row['road_name'] in roads_and_regions:
            temp = [row['local_authority_name']]
            roads_and_regions[row['road_name']] = temp

        else:
            found = False
            for i in roads_and_regions[row['road_name']]:
                if row['local_authority_name'] == i:
                    found = True
            if not found:
                roads_and_regions[row['road_name']].append(row['local_authority_name'])

    for road in roads_and_regions:
        n = 0
        temp = []
        temp = roads_and_regions[road]
        for i in roads_and_regions[road]:
            if n > 0:
                G1.AddEdge(region_to_index[i], region_to_index[temp[n - 1]])
            n += 1

    snap.DrawGViz(G1, snap.gvlNeato, "graph.png", "Scotland's Roads", True, NIdColourH)
    snap.DrawGViz(G1, snap.gvlNeato, "output.png", "Scotland's Roads", label)


main()
