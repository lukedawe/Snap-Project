import snap
import pandas as pd
import os
import time

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

header = "UK's Roads"


# Opens the file
def open_file():
    # read in the file using panda
    data = pd.read_csv(r'Scotland_2018.csv', sep=',', error_bad_lines=False, index_col=False, dtype='unicode',
                       low_memory=False)
    data = data.round(3)
    return data


def main():
    # keeps an eye on the time the program takes to complete
    start_time = time.time()
    data = open_file()
    df = process_data(data)
    print(df)
    generate_graph(df)
    print("Complete")
    print("--- %s seconds ---" % (time.time() - start_time))


# discard the columns that are not needed and puts the data that is into a data frame
def process_data(data):
    df = pd.DataFrame(data, columns=['road_name', 'local_authority_name', 'all_motor_vehicles'])
    return df


# simple function to search the array for a region name
def search_array(name, array):
    i = 0
    # goes along every element of the array, checking if it is
    # the same as the name that is being searched for
    while i < len(array):
        if name == array[i]:
            return True
        i += 1
    return False


# determines the colour of the node, return the colour
# this is for making the heat-map-style diagram
def node_colour(num):
    if num < 80000:
        return "blue"
    elif 80000 < num < 150000:
        return "cyan"
    elif 150000 < num < 200000:
        return "green"
    elif 200000 < num < 400000:
        return "yellow"
    elif 400000 < num < 800000:
        return "orange"
    elif 800000 < num < 1700000:
        return "red"
    else:
        return "purple"


# generate both output graphs
def generate_graph(df):
    # set up 3 python dictionaries
    # roads_and_regions stores the roads and an array of all the regions that each road passes through
    roads_and_regions = {}
    # regions_to_traffic stores all the regions and their related traffic data
    regions_to_traffic = {}
    # region_array stores a list of all of the regions
    region_array = []
    # region_to_index stores each region to its related index in the spreadsheet
    # this is for the edges when making the graph
    region_to_index = {}
    G1 = snap.TUNGraph.New()
    # store all of the labels
    label = snap.TIntStrH()
    # store all of the colours for the heat map
    NIdColourH = snap.TIntStrH()

    # note that the reason one graph cannot contain the colours and the labels is because the two lines
    # of code above are the same data type and the snap.DrawGViz function cannot determine which is which

    # go along each row in the data frame
    for index, row in df.iterrows():

        # if the local authority has not already been seen, add it to region_array, region_to_index, the graph (G1),
        # regions_to_traffic and store the label
        if not search_array(row['local_authority_name'], region_array):
            region_array.append(row['local_authority_name'])
            region_to_index[row['local_authority_name']] = index
            G1.AddNode(index)
            label[index] = row['local_authority_name']
            regions_to_traffic[row['local_authority_name']] = int(row['all_motor_vehicles'])
        # otherwise, add the traffic count to the regions_to_traffic dictionary
        else:
            t = int(regions_to_traffic[row['local_authority_name']]) + int(row['all_motor_vehicles'])
            regions_to_traffic[row['local_authority_name']] = t

        # if we have not seen this road before in the roads_and_regions dictionary, add it to the dictionary
        if not row['road_name'] in roads_and_regions:
            # make it an array so that the dictionary stores arrays and not strings
            # this allows us to use "append" later on
            temp = [row['local_authority_name']]
            roads_and_regions[row['road_name']] = temp
        # if we have already seen this road before in the dictionary, check to see if we already know that the
        # road has passed through this region
        else:
            if not search_array(row['local_authority_name'], roads_and_regions[row['road_name']]):
                roads_and_regions[row['road_name']].append(row['local_authority_name'])

    # for each of the roads in the roads_and_regions dictionary...
    for road in roads_and_regions:

        n = 0
        temp = roads_and_regions[road]
        for i in roads_and_regions[road]:
            # start at the second element, if there is one, and make a link between that element
            # and the one before, repeat this process
            if n > 0:
                G1.AddEdge(region_to_index[i], region_to_index[temp[n - 1]])
            n += 1

    # for each of the regions in the regions_to_traffic dictionary...
    for region in regions_to_traffic:
        # set the colour to whatever the node_colour function decides based on the traffic data
        NIdColourH[region_to_index[region]] = node_colour(regions_to_traffic[region])

    # draw both graphs
    snap.DrawGViz(G1, snap.gvlNeato, "graph.png", header, True, NIdColourH)
    snap.DrawGViz(G1, snap.gvlNeato, "output.png", header, label)


main()
