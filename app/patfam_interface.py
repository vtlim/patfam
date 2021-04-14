#!/usr/bin/env python3

"""
TODO
add description

TODO

front-end hook ups:
 1. input numbers and app types
 2. disable submit button if 0 inputs
 3. pass json result to output graph

code structure
 1. async parallel processing for diff jurisdictions (except uspto first)

unit tests
 * get_wipo_identifiers (target page)
 * get_wipo_identifiers (front page)

manual tests
 * throw in an unrelated entry: 09/593,589
 * what if there are two distinct families

"""


import re
import matplotlib.pyplot as plt

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, write_dot
from networkx.readwrite import json_graph


from get_uspto import get_uspto_continuity
from get_wipo import get_wipo_identifiers
from get_epo import get_epo_priorities


# TODO: include functionality for inputDocType of patno
list_of_inputs = [
    {"inputNo":"09/418,640",     "inputDocType":"application", "jurisdiction":"uspto"}, # level 0
    {"inputNo":"10/110,512",     "inputDocType":"application", "jurisdiction":"uspto"}, # level 2
    {"inputNo":"PCT/US00/27963", "inputDocType":"application", "jurisdiction":"wipo"},  # level 1
    {"inputNo":"WO 01/29057",    "inputDocType":"publication", "jurisdiction":"wipo"},  # level 1 (equiv)
    {"inputNo":"EP00970724",       "inputDocType":"application", "jurisdiction":"epo"},   # level 2
    #{"inputNo":"970724.1",       "inputDocType":"application", "jurisdiction":"epo"},   # level 2 (see pad number comment below; start with above line first)
    {"inputNo":"2001-531855",    "inputDocType":"application", "jurisdiction":"jpo"},   # level 2
]
num_inputs = len(list_of_inputs)


def check_relation(fam_dict, last_n_chars, ref_value, fam_node, ref_node):
    """
    Check whether any document identifiers in fam_dict (whether in parent or
    child keys) matches that of ref_value. If a match is found, add an
    edge between the queried and reference nodes in the graph.

    TODO
    """

    found_a_relation = False

    if last_n_chars == 0:
        last_n_chars = len(ref_value)

    # check if in parent []
    this_famdata_parent = fam_dict["parent"]
    for value in this_famdata_parent:
        print("\tchecking ", value, "against reference: ", ref_value)
        if ( value[-last_n_chars:] == ref_value[-last_n_chars:] ):
            print("\t > found match\n")

            # add edge from parent to child
            DG.add_edge(ref_node, fam_node)
            found_a_relation = True
            break

    if found_a_relation:
        return found_a_relation

    # check if in child []
    this_famdata_child = fam_dict["child"]
    for value in this_famdata_child:
        print("\tchecking ", value, "against reference: ", ref_value)
        if ( value[-last_n_chars:] == ref_value[-last_n_chars:] ):
            print("\t > found match\n")

            # add edge from parent to child
            DG.add_edge(fam_node, ref_node)
            found_a_relation = True
            break

    return found_a_relation



# generate a directed graph with nodes for each input
DG = nx.DiGraph()
input_numbers = [ sub["inputNo"] for sub in list_of_inputs ]
DG.add_nodes_from(input_numbers)
#DG.add_edge(input_numbers[0], input_numbers[0])

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
# obtain data from uspto api
# ================================================
print("\n\nRetrieving USPTO data...")

for entry in inputs_uspto:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    print(f"  Input entry: {curr_input}")

    # remove any spaces, punctuation (keep numbers/letters)
    proc_input = re.sub(r'[^a-zA-Z0-9]', '', curr_input)

    # if pubNo without kind code (A*) specified, append an "A1"
    if (curr_type == "publication") and ("A" not in proc_input):
        proc_input = proc_input + "A1"

    # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if curr_input == "09/418,640": entry["famData"] = {'parent': [], 'child': ['PCT/US00/27963'], 'uncategorized': []}
    if curr_input == "10/110,512": entry["famData"] = {'parent': [], 'child': [], 'uncategorized': []}
    continue
    # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # make api request
    try:
        data_uspto = get_uspto_continuity(proc_input, doc_type=curr_type)
    except AssertionError:
        pass
        #f"Unable to reach USPTO Patent Examination Data System. Please try again in a few moments."

    if data_uspto == "ERROR":
        continue
        # TODO
        # f'Sorry, {curr_input_type} "{proc_input}" cannot be retrieved as entered.'
        # f'Please re-enter the application number in the format: 15123456, or try a new search.'
        # f'Please re-enter the publication number in the format: US20190123456A1, or try a new search.'
    else:
        entry["famData"] = data_uspto


# ================================================
# obtain data from epo api
# ================================================
print("\n\nRetrieving EPO data...")

for entry in inputs_epo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    print(f"  Input entry: {curr_input}")

    # remove any spaces, punctuation (keep numbers/letters)
    proc_input = re.sub(r'[^a-zA-Z0-9]', '', curr_input)

    # TODO - broken - pad number to go from 970724.1 to EP00970724

    ## >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #if curr_input = "EP00970724": entry["famData"] = {'parent': ['WO2000US27963', 'US19990418640'], 'child': [], 'uncategorized': []}
    #continue
    ## >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # TODO try/except
    # make api request
    data_epo = get_epo_priorities(proc_input, doc_type=curr_type)

    if data_epo == "ERROR":
        continue
        # TODO
        # f'Sorry, {curr_input_type} "{proc_input}" cannot be retrieved as entered.'
        # f'Please re-enter the application number in the format: 15123456, or try a new search.'
        # f'Please re-enter the publication number in the format: US20190123456A1, or try a new search.'
    else:
        entry["famData"] = data_epo
    print(data_epo)


# ================================================
# obtain data from wipo scraping
# ================================================
print("\n\nRetrieving WIPO data...")

for entry in inputs_wipo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    print(f"  Input entry: {curr_input}")

    # if input is appNo AND contains "PCT" and "US"
    # check if we already identified it in uspto results
    if curr_type == "application" and (
        "PCT" in curr_input and "US" in curr_input):

        # get uspto entries having famdata
        uspto_with_famdata = [ sub for sub in inputs_uspto if
            "famData" in sub ]

        # check whether any of the uspto entr(ies) are related to this pct
        for subentry in uspto_with_famdata:

            # only check last five digits to account for cases like:
            # PCT/US00/27963 == PCT/US2000/027963
            check_relation(
                subentry["famData"], 5, curr_input,
                subentry["inputNo"], curr_input)

        # subentry_relations.append( ... )
        #if not any(subentry_relations):
        # also use the uspto api to check the pct/us num
        # possibly redundant, but consider counterexample:
        # [09/418,640 ==> {PCT/US00/27963] ==> 10/110,512 (abandoned)}

        # make api request
        # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        data_wipo_uspto = {'parent': ['09418640'], 'child': ['10110512'], 'uncategorized': []}
        # >>>>>>>>>>>>>>>>>>>>>>>>>>> TESTING MODE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #try:
        #    data_wipo_uspto = get_uspto_continuity(curr_input, doc_type=curr_type)
        #except AssertionError:
        #    data_wipo_uspto = "ERROR"
        #    #f"Unable to reach USPTO Patent Examination Data System. Please try again in a few moments."


        # handle error (TODO: create class of errors in this doc for indiv juris)
        if data_wipo_uspto == "ERROR":
            continue
        else:
            entry["famData"] = data_wipo_uspto

        # with inputs_uspto as reference, check wipo search result (6 digits)
        # check all inputs_uspto, not just those that have famData
        for subentry in inputs_uspto:

            subentry_val = re.sub(r'[^a-zA-Z0-9]', '',
                subentry["inputNo"])

            check_relation(data_wipo_uspto, 6, subentry_val,
                curr_input, subentry["inputNo"])

        # move onto next entry (don't search PCT/USxx/xxxx in Patentscope)
        continue


    # remove any spaces, punctuation (keep numbers/letters/fwd slashes)
    proc_input = re.sub(r'[^a-zA-Z0-9\/]', '', curr_input)

    # scrape with selenium
    data_wipo = get_wipo_identifiers(proc_input, doc_type=curr_type)

    if data_wipo == "UNDEFINED":
        # "The PatentScope search query was unsuccessful."
        continue
    else:
        entry["famData"] = data_wipo

    # with inputs_uspto as reference, check wipo search result (6 digits)
    # check all inputs_uspto, not just those that have famData
    for subentry in inputs_uspto:

        subentry_val = re.sub(r'[^a-zA-Z0-9]', '',
            subentry["inputNo"])

        check_relation(data_wipo, 6, subentry_val,
            curr_input, subentry["inputNo"])

# ================================================
# obtain data from jpo scraping
# ================================================
print("\n\nRetrieving JPO data...")
for entry in inputs_jpo:
    curr_input = entry["inputNo"]
    curr_type = entry["inputDocType"]
    print(f"  Input entry: {curr_input}")

    # TODO
    continue

# ================================================
# identify relationships not found earlier
# ================================================
print("\n\n")
print(inputs_uspto)
print(inputs_wipo)

# ================================================
# process results to send to app
# ================================================
# print(inputs_uspto, inputs_wipo, inputs_epo, inputs_jpo)
# print(list(DG.edges))


# show hierarchical tree with matplotlib/pygraphviz
# https://stackoverflow.com/a/11484144
pos = graphviz_layout(DG, prog='dot')
nx.draw(DG, pos, with_labels=True, arrows=True)
plt.show()

## plot separately in graphviz since self-edges are difficult in mpl
## run: dot -Tpng graph.dot > graph.png
## https://stackoverflow.com/a/22315199
#write_dot(DG,'graph.dot')

# separate the unconnected nodes into a different graph
# https://stackoverflow.com/a/48820766
orig_nodes = list(DG.nodes)
DG_orphans = nx.isolates(DG)
DG.remove_nodes_from(list(DG_orphans))
new_nodes = list(DG.nodes)
rm_nodes = list(set(orig_nodes) - set(new_nodes))
print(f"\n\nOriginal set of nodes: {orig_nodes}")
print(f"Isolated nodes removed: {rm_nodes}")

print("\n\nsome json outputs:")
print(json_graph.node_link_data(DG))
print(json_graph.tree_data(DG, root=list(DG.nodes)[0]))
