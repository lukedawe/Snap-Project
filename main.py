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
    df = pd.DataFrame(data, columns=['road_name', 'local_authority_name', 'all_motor_vehicles'])
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
    #roads_and_regions.setcdefault("", [])
    region_array = []
    region_to_index = {}
    previous = ""
    num_of_vehicles = 0
    G1 = snap.TUNGraph.New()
    label = snap.TIntStrH()
    NIdColourH = snap.TIntStrH()
    index_to_add_to = 0

    for index, row in df.iterrows():
        if previous == "":
            num_of_vehicles = int(row['all_motor_vehicles'])
        elif previous == row['local_authority_name']:
            num_of_vehicles += int(row['all_motor_vehicles'])
        else:
            num_of_vehicles = int(row['all_motor_vehicles'])
            index_to_add_to = index

        previous = row['local_authority_name']

        if num_of_vehicles < 100000:
            NIdColourH[index_to_add_to] = "blue"
        elif 100000 < num_of_vehicles < 200000:
            NIdColourH[index_to_add_to] = "cyan"
        elif 200000 < num_of_vehicles < 500000:
            NIdColourH[index_to_add_to] = "green"
        elif 500000 < num_of_vehicles < 700000:
            NIdColourH[index_to_add_to] = "yellow"
        elif 700000 < num_of_vehicles < 900000:
            NIdColourH[index_to_add_to] = "orange"
        elif 900000 < num_of_vehicles < 2000000:
            NIdColourH[index_to_add_to] = "red"
        else:
            NIdColourH[index_to_add_to] = "purple"

        if not search_array(row['local_authority_name'], region_array):
            region_array.append(row['local_authority_name'])
            region_to_index[row['local_authority_name']] = index
            G1.AddNode(index)
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