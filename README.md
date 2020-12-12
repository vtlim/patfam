# PatFam: Explore Patent Families

About: TBD

## Setup

### [USPTO] [USPTO Open Data API Client](https://docs.ip-tools.org/uspto-opendata-python/index.html)
For USPTO data, we will use the API client for the USPTO Patent Examination Data System (PEDS). Do not mix up PEDS with PBD, which is the USPTO PAIR Bulk Data (PBD) system. The PBD has been decommissioned.

```
# install libxml2 dependencies (make sure you have -dev versions)
sudo apt-get install libxml2-dev libxslt1-dev python-lxml

# create conda environment and install some packages (see note below)
conda create -n patents python=3.6
conda activate patents
conda install -c anaconda lxml
conda install pip

# install the api client
pip install uspto-opendata-python

# run a test query
uspto-peds get "15431686" --type=application --format=xml
```
NOTE: As of Dec. 2020, `uspto-opendata-python` will not install if using Python 3.9.0 (returning gcc compilation error of [this type](https://github.com/pandas-dev/pandas/issues/32114)).
