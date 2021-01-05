#!/usr/bin/env python3

"""
TODO
add description


front-end hook ups:
 1. inputs
 2. can't submit if zero inputs (1 is ok i think)

code structure
 1. async parallel processing for diff jurisdictions

"""


import re
import matplotlib.pyplot as plt

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, write_dot


from get_uspto_continuity import get_uspto_continuity
from get_wipo_identifiers import get_wipo_identifiers


# TODO: include functionality for inputDocType of patno
list_of_inputs = [
    {"inputNo":"09/418,640",     "inputDocType":"application", "jurisdiction":"uspto"},
    {"inputNo":"PCT/US00/27963", "inputDocType":"application", "jurisdiction":"wipo"},
    {"inputNo":"WO 01/29057",    "inputDocType":"publication", "jurisdiction":"wipo"},
    {"inputNo":"970724.1",       "inputDocType":"application", "jurisdiction":"epo"},
    {"inputNo":"2001-531855",    "inputDocType":"application", "jurisdiction":"jpo"},
]
num_inputs = len(list_of_inputs)

# generate a directed graph with nodes for each input
DG = nx.DiGraph()
input_numbers = [ sub["inputNo"] for sub in list_of_inputs ]
DG.add_nodes_from(input_numbers)

DG.add_edge(input_numbers[0], input_numbers[0])

# separate input entries by jurisdiction
inputs_uspto = [ sub for sub in list_of_inputs if
    sub['jurisdiction'] == "uspto" ]
inputs_epo = [ sub for sub in list_of_inputs if
    sub['jurisdiction'] == "epo" ]
inputs_wipo = [ sub for sub in list_of_inputs if
    sub['jurisdiction'] == "wipo" ]
inputs_jpo = [ sub for sub in list_of_inputs if
    sub['jurisdiction'] == "jpo" ]

# ================================================
# obtain data by each jurisdiction
# ================================================

# get data from uspto api
print("Retrieving USPTO data...")

for entry in inputs_uspto:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]

    # remove any spaces, punctuation (leave numbers/letters)
    proc_input = re.sub(r'[^a-zA-Z0-9]', '', curr_input)

    # if pubNo without kind code (A*) specified, append an "A1"
    if (curr_type == "publication") and ("A" not in proc_input):
        proc_input = proc_input + "A1"

    # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    entry["famData"] = {'parent': [], 'child': ['PCT/US00/27963'], 'uncategorized': []}
    continue
    # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # make api request
    data_uspto = get_uspto_continuity(proc_input, doc_type=curr_type)

    if data_uspto == "ERROR":
        continue
        # TODO
        # f'Sorry, {curr_input_type} "{proc_input}" cannot be retrieved as entered.'
        # f'Please re-enter the application number in the format: 15123456, or try a new search.'
        # f'Please re-enter the publication number in the format: US20190123456A1, or try a new search.'
    else:
        entry["famData"] = data_uspto


# get data from epo api
print("Retrieving EPO data...")

for entry in inputs_epo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    continue

# get data from wipo scraping
print("Retrieving WIPO data...")

for entry in inputs_wipo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]

    # if input is appNo AND contains "PCT" and "US"
    # check if we already identified it in uspto results
    if curr_type == "application" and (
        "PCT" in curr_input and "US" in curr_input):

        # only check last five digits to account for cases like:
        # PCT/US00/27963 == PCT/US2000/027963
        last_five_digits = curr_input[-5:]

        # get uspto entries having famdata
        uspto_with_famdata = [ sub for sub in inputs_uspto if
            "famData" in sub ]

        for subentry in uspto_with_famdata:

            # check if in parent []
            this_famdata_parent = subentry["famData"]["parent"]
            for value in this_famdata_parent:
                if value[-5:] == last_five_digits:
                    # add edge from parent to child
                    DG.add_edge(curr_input, subentry["inputNo"])
                    continue

            # check if in child []
            this_famdata_child = subentry["famData"]["child"]
            for value in this_famdata_child:
                if value[-5:] == last_five_digits:
                    # add edge from parent to child
                    DG.add_edge(subentry["inputNo"], curr_input)
                    continue

    # remove any spaces, punctuation (leave numbers/letters)
    proc_input = re.sub(r'[^a-zA-Z0-9]', '', curr_input)

    # scrape with selenium
    data_wipo = get_wipo_identifiers(proc_input, doc_type=curr_type)

    if data_wipo == "UNDEFINED":
        continue
    # "The PatentScope search query returned too many results. Try a more definitive input number."



# get data from jpo scraping
print("Retrieving JPO data...")
for entry in inputs_jpo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    continue

print(inputs_uspto, inputs_wipo, inputs_epo, inputs_jpo)


# show hierarchical tree with matplotlib/pygraphviz
# https://stackoverflow.com/a/11484144
# TODO: networkx custom images on nodes, of uniform area
pos = graphviz_layout(DG, prog='dot')
nx.draw(DG, pos, with_labels=True, arrows=True)
plt.show()

# plot separately in graphviz since self-edges are difficult in mpl
# run: dot -Tpng graph.dot > graph.png
# https://stackoverflow.com/a/22315199
write_dot(DG,'graph.dot')

