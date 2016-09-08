
# coding: utf-8

# ## SOU text files to Solr database
# This script will pre-process the text files, then add them to the Solr database. First, create a Sorl database with:
#
#  sudo su - solr -c "/opt/solr/bin/solr create -c sou -n data_driven_schema_configs"
#
# Then make sure there is a text_sv schema using the Sorl web interface.

# In[9]:

import csv
import re
from os import listdir
import pysolr


# Change this to reflect your core name
solr = pysolr.Solr('http://localhost:8983/solr/sou/', timeout=1000)


# In[11]:

def tokens(text):
    words = re.findall('[A-ZÅÄÖ]|[a-zåäö]+|[\d+]', text)
    return ' '.join(words)


# In[12]:

limit = 9
counter = 0
# Change directories to where the documents are stored.
for filename in listdir(u"//home/changedirectory/SOU19222015/"):
    with open("//home/changedirectory/SOU19222015/" + filename, encoding='utf-8') as currentfile:
        text = currentfile.read()
        soutext = tokens(text)
        regexpgrep = re.findall(r'(\d\d\d\d)\_(\d+)', filename)
        year = regexpgrep[0][0]
        number = regexpgrep[0][1]
        yearnumber = year + ":" + number

        solr.add([
                {
                    "id": counter,
                    "year": year,
                    "number": number,
                    "filename": filename,
                    "fulltext": text,
                },
            ])


        counter = counter + 1

        print("Added successfully: " + str(counter))
