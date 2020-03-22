import snap
import csv
import pandas as pd
import os
import numpy as np
import time

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

header = "UK's Roads"

# Opens the file
def open_file():
    data = pd.read_csv(r'data.csv', sep=',', error_bad_lines=False, index_col=False, dtype='unicode',
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
    df = pd.DataFrame(data, columns=['road_name', 'local_authority_name', 'all_motor_vehicles'])
    return df


def search_array(name, array):
    i = 0
    while i < len(array):
        if name == array[i]:
            return True
        i += 1
    return False


def node_colour(num):
    if num < 5000000:
        return "blue"
    elif 5000000 < num < 10000000:
        return "cyan"
    elif 10000000 < num < 15000000:
        return "green"
    elif 15000000 < num < 20000000:
        return "yellow"
    elif 20000000 < num < 30000000:
        return "orange"
    elif 30000000 < num < 50000000:
        return "red"
    else:
        return "purple"


def generate_graph(df):
    roads_and_regions = {}
    regions_to_traffic = {}
    region_array = []
    region_to_index = {}
    previous = ""
    num_of_vehicles = 0
    G1 = snap.TUNGraph.New()
    label = snap.TIntStrH()
    NIdColourH = snap.TIntStrH()
    index_to_add_to = 0

    for index, row in df.iterrows():

        if not search_array(row['local_authority_name'], region_array):
            region_array.append(row['local_authority_name'])
            region_to_index[row['local_authority_name']] = index
            G1.AddNode(index)
            label[index] = row['local_authority_name']
            regions_to_traffic[row['local_authority_name']] = int(row['all_motor_vehicles'])
        else:
            t = int(regions_to_traffic[row['local_authority_name']]) + int(row['all_motor_vehicles'])
            regions_to_traffic[row['local_authority_name']] = t

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

    for region in regions_to_traffic:
        NIdColourH[region_to_index[region]] = node_colour(regions_to_traffic[region])

    snap.DrawGViz(G1, snap.gvlNeato, "graph.png", header, True, NIdColourH)
    snap.DrawGViz(G1, snap.gvlNeato, "output.png", header, label)


main()