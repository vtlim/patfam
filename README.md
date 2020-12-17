# PatFam: Patent Families

_README last edited_: 16 Dec 2020

The purpose of this tool is to allow users to easily determine whether patent applications are in the same family. Instead of having to check each individual patent office's website, users can enter patent, application, or publication numbers for various patent offices and see the relationship between the documents. 

Currently supports: TBD

## Setup

### [USPTO] [USPTO Open Data API Client](https://docs.ip-tools.org/uspto-opendata-python/index.html)
For data from the United States Patent and Trademark Office (USPTO), we'll use the API client for the USPTO Patent Examination Data System (PEDS). Do not mix up PEDS with PBD, which is the USPTO PAIR Bulk Data (PBD) system. The PBD has been decommissioned.

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

#### See my tutorial walkthrough of the USPTO Open Data API Client [here](uspto/explore_uspto_data.ipynb).

### [EPO] [Python EPO OPS Client](https://github.com/gsong/python-epo-ops-client)
For data from the European Patent Office (EPO), we'll use the Open Patent Services (OPS) client developed by George Song et al. In order to get API access, you will need to [request access credentials](https://developers.epo.org/) from OPS. After I submitted my request, I was granted access from EPO the next day.
```
conda activate patents
pip install python-epo-ops-client
```
#### See my tutorial walkthrough of the Python EPO OPS Client [here](epo/explore_epo_data.ipynb).

### Web Scraping

As far as I can tell, there is no freely available API access to the World Intellectual Property Organization (WIPO; for PCT applications) or to the Japan Patent Office (JPO). For those applications, we'll request data from the web directly.

Before this I tried the Python `requests` package to obtain site data. I made a GET search query to WIPO PatentScope for `docId=WO2001029057`. However, no patent-related data could be found in the HTML content. It looks like the site is rendered dynamically using JavaScript so we'll use Selenium instead:

```
conda activate patents
conda install -c conda-forge selenium
```

Since I'm working in the Windows Subsystem for Linux (WSL2), I needed to download an Internet browser and related driver (following the [tutorial](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/) from Greg Brisebois). If you already have an Internet browser in the same OS that you're working in, you would just get to obtain the relevant driver for your browser, browser version, and OS.


```
# install dependencies
sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

# get chrome browser
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# check browser install
google-chrome --version

# get chrome driver; USE THE DRIVER VERSION RELEVANT TO YOUR SETUP
wget https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

# check driver install
chromedriver --version
```

Optionally, if you want to work with the Chrome window (as opposed to using it in "headless form"), try the command `google-chrome` to check that the window will come up. I had to resolve a few issues with WSL2 on my end before it worked. More details [here](https://github.com/vtlim/patfam/blob/main/wsl2_xserver.md).

#### See an example of using Selenium to obtain WIPO PatentScope data [here](wipo/explore_wipo_data.ipynb).
#### See an example of using Selenium to obtain JPO patent data [here](jpo/explore_jpo_data.ipynb).
