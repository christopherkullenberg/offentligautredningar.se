#coding: utf-8
'''
SOU text files to Solr database

This script will pre-process the text files, then add them to the Solr database. 
First, create a Sorl database with:

  sudo su - solr -c "/opt/solr/bin/solr create -c sou -n data_driven_schema_configs"

Then add the following schema to the core:

year - int
number - int
filename - string
url - string
fulltext - text_sv

'''

import csv
import re
from os import listdir
import pysolr
import sqlite3

'''
This database contains the URLs according to the following schema:
CREATE TABLE main (id INT PRIMARY KEY, year INT, number INT, url TEXT);
'''
conn = sqlite3.connect('SOUpdfURLMerged.sqlite3') 

def querydb(year, number):
    '''Returns URL if there is one in DB'''
    search = conn.execute('SELECT * FROM main WHERE year=(?) AND number=(?)', (year, number, ))
    url = "notfound.html"
    for s in search:
        url = s[3]
    return(url)


# Change this to reflect your core name
solr = pysolr.Solr('http://localhost:8983/solr/sou/', timeout=1000)

# tokenizer for the fulltext
def tokens(text):
    words = re.findall('[A-ZÅÄÖ]|[a-zåäö]+|[\d+]', text)
    return ' '.join(words)

limit = 9
counter = 0
# Change directories to where the documents are stored.
for filename in listdir(u"//home/chrisk/www/offentligautredningar.se/source/"):
    with open("//home/chrisk/www/offentligautredningar.se/source/" + filename, encoding='utf-8') as currentfile:
        text = currentfile.read()
        soutext = tokens(text)
        regexpgrep = re.findall(r'(\d\d\d\d)\_(\d+)', filename)
        year = regexpgrep[0][0]
        number = regexpgrep[0][1]
        yearnumber = year + ":" + number
        url = querydb(year, number)
        solr.add([
                {
                    "id": counter,
                    "year": year,
                    "number": number,
                    "filename": filename,
                    "pdfurl": url,
                    "fulltext": text,
                },
            ])


        counter = counter + 1

        print("Added successfully: " + str(counter))
        print("SOU " + year + ":" + number + " " + url) 
        print("---") 
