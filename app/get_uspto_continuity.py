#!/usr/bin/env python3

import json
from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.util.client import NoResults


def get_uspto_continuity(input_num, doc_type):
    """
    todo

    Parameters
    ----------
    input_num : string
        alphanumeric identifier of document
    doc_type : string
        valid options are 'application' 'publication' 'patent'

    Returns
    -------
    the string "ERROR" for no results else a dictionary of data, e.g.,
        {"parent": list_of_parent_data,
         "child": list_of_child_data,
         "uncategorized": list_of_data}

    """

    # create api client
    client = UsptoPatentExaminationDataSystemClient()

    # make request and handle potential null result
    try:
        result = client.download_document(number=input_num, type=doc_type,
            format='json')
    except NoResults:
        return "ERROR"

    # process json result
    doc_byte_str = result['json']
    doc_dict = json.loads(doc_byte_str.decode('utf-8'))
    doc_fam = doc_dict['PatentData'][0][
        'patentCaseMetadata'][
        'relatedDocumentData'][
        'parentDocumentDataOrChildDocumentData']

    # categorize results then return
    fam_parent = []
    fam_child = []
    fam_uncategorized = []

    for entry in doc_fam:

        if "parentDocumentStatusCode" in entry:
            fam_parent.append(entry["applicationNumberText"])

        elif "childDocumentStatusCode" in entry:
            fam_child.append(entry["applicationNumberText"])

        else:
            fam_uncategorized.append(entry["applicationNumberText"])

    result = { "parent": fam_parent,
        "child": fam_child,
        "uncategorized": fam_uncategorized }

    return result


"""
13/780,955

{'descriptionText': 'This application is a Continuation of', 'applicationNumberText': '13548784', 'filingDate': '2012-07-13', 'aiaIndicator': False, 'parentDocumentStatusCode': 'Patented', 'patentNumber': '8410074'}
{'descriptionText': 'This application is a Continuation of', 'applicationNumberText': '12550479', 'filingDate': '2009-08-31', 'aiaIndicator': False, 'parentDocumentStatusCode': 'Abandoned', 'patentNumber': ''}
{'descriptionText': 'This application is a Continuation of', 'applicationNumberText': '12184379', 'filingDate': '2008-08-01', 'aiaIndicator': False, 'parentDocumentStatusCode': 'Patented', 'patentNumber': '7601700'}
{'descriptionText': 'This application is a Division of', 'applicationNumberText': '10571339', 'filingDate': '2006-11-29', 'aiaIndicator': False, 'parentDocumentStatusCode': 'Patented', 'patentNumber': '7425544'}
{'descriptionText': 'This application is National Stage Entry of', 'applicationNumberText': 'PCT/US2004/030436', 'filingDate': '2004-09-17', 'parentDocumentStatusCode': '-', 'patentNumber': ''}
{'descriptionText': 'This application Claims Priority from Provisional Application', 'applicationNumberText': '60576534', 'filingDate': '2004-06-03', 'parentDocumentStatusCode': 'Expired', 'patentNumber': ''}
{'descriptionText': 'This application Claims Priority from Provisional Application', 'applicationNumberText': '60504110', 'filingDate': '2003-09-18', 'parentDocumentStatusCode': 'Expired', 'patentNumber': ''}
{'descriptionText': 'which is Abandoned claims the benefit of 13780955', 'applicationNumberText': '14330213', 'filingDate': '2014-07-14', 'childDocumentStatusCode': 'Abandoned', 'patentNumber': ''}
"""
