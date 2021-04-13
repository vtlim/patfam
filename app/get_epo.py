#!/usr/bin/env python3

import os
import epo_ops


def initiate_api_call():

    # get api access keys
    my_key = os.getenv("EPO_KEY")
    my_secret_key = os.getenv("EPO_SECRET_KEY")

    # instantiate client
    client = epo_ops.Client(
        key=my_key,
        secret=my_secret_key, accept_type='json'
    )

    print(dir(client))
    return client

def get_epo_priorities(input_num, doc_type):

    client = initiate_api_call()

    # TODO try/except somewhere here or the next line
    response = client.published_data(
        reference_type = doc_type,
        input = epo_ops.models.Epodoc(input_num),
        endpoint = 'biblio',
        constituents = ['biblio'])

    # pull out json data
    mydata = response.json()

    # get list of priority claim information out of mydata
    pc_data = mydata['ops:world-patent-data'][
        'exchange-documents'][
        'exchange-document'][
        -1][
        'bibliographic-data'][
        'priority-claims'][
        'priority-claim']

    pc_list = []
    for pc in pc_data:
        pc_list.append(pc['document-id'][0]['doc-number']['$'])

    return { "parent": pc_list, "child": [], "uncategorized": [] }

