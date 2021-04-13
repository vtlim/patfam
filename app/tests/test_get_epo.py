"""
test_get_epo.py
"""
import sys, os
import epo_ops

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.." ))
from get_epo import initiate_api_call, get_epo_priorities

def test_epo_data():
    result = get_epo_priorities('EP00970724', 'application')
    assert 'WO2000US27963' in result['parent']
    assert 'US19990418640' in result['parent']

def test_epo_client():
    client = initiate_api_call()

    response = client.published_data(              # Retrieve bibliography data
      reference_type = 'application',              # publication, application, priority
      input = epo_ops.models.Epodoc('EP00970724'), # original, docdb, epodoc
      endpoint = 'biblio',                         # optional, defaults to biblio in case of published_data
      constituents = ['biblio']                    # optional, e.g., full-cycle, images, biblio, abstract
    )

    assert response.status_code == 200

"""
{'parent': ['WO2000US27963','US19990418640'], 'child': [], 'uncategorized': []}
"""
