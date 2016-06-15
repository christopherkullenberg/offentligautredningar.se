#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
PROTOTYPE SCRIPT ONLY
'''

# Import modules for CGI handling and UTF-8 handling of input/output
import cgi, cgitb
import sys
import re
import os
import pysolr
#import numpy as np
#import collections
#import pandas as pd
#from bokeh.plotting import figure, output_file, save
#from bokeh.embed import file_html
#from bokeh.resources import CDN

# Fix IO and utf8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


solr = pysolr.Solr('http://localhost:8983/solr/souprototype/', timeout=10)

# Get data from fields
form = cgi.FieldStorage()
if form.getvalue('search_word'):
    form_string = form.getvalue('search_word')
    search_string = form_string
else:
    search_string = "Not entered"

if form.getvalue('result_limit'):
    result_limit = form.getvalue('result_limit')
else:
    result_limit = 10

if form.getvalue('metod'):
    themetod = form.getvalue('metod')
    if themetod == "simple":
        metod = "simple"
    elif themetod == "advanced":
        metod = "advanced"
    else:
        metod = "simple"

if form.getvalue('order'):
    theorder = form.getvalue('order')
    if theorder == "Stigande":
        order = "year asc"
    elif theorder == "Fallande":
        order = "year desc"
    else:
        order = "year desc"

# Change this when there are multiple modes
mode = 'match'

'''
This is a bokeh time graph that takes year/frequency and turns it into
a time series diagram. Not used in prototype.
# Fix date before can be used
def graph():
    datelist = []
    for date in results:
        # [:-17] will return %Y-%m and [:-14] will return %Y-%m-%d
        thedate = date[1][:-14]
        datelist.append(thedate)

    counter = collections.Counter(datelist)
    output_file("/Directory", title="Resultat")
    years = []
    val   = []
    yearvaldict = {}

    for number in sorted(counter):
        years.append(number)
        value = counter[number]
        val.append(value)
        yearvaldict[number] = [value]

    #for key, value in yearvaldict.items():
    #    print(key, value)

    # Convert data into a panda DataFrame format
    data=pd.DataFrame({'year':years, 'value':val}, )

    # Create new column (yearDate) equal to the year Column but with datetime format
    data['yearDate']=pd.to_datetime(data['year'],format='%Y-%m-%d')

    # Create a line graph with datetime x axis and use datetime column(yearDate)
    # for this axis
    p = figure(width=1000, height=250, x_axis_type="datetime")
    p.logo = None
    p.toolbar_location = "right"
    p.line(x=data['yearDate'],y=data['value'], color="#9B287B", line_width=2)
    #show(p) # for debugging
    bokehhtml = file_html(p, CDN, "Resultat")
    save(p)
    return(bokehhtml)
'''

# Just printing some headers.
print("Content-type:text/html; charset=utf-8\r\n\r\n")
print()
#print(graph())

print('''<style>
    table#t01 tr:nth-child(even) {
    background-color: #eee;
    }
    table#t01 tr:nth-child(odd) {
    background-color: #fff;
    }
    table#t01 th {
    color: white;
    background-color: black;
    }
    td#d01 {
    padding: 15px;
    }
    span.highlight {
    background-color: yellow;
    }
    </style>
    ''')

results = solr.search(search_string, rows = result_limit, sort = order)

print('<p>Du sökte på ordet <b>' + search_string + '</b> i ' + mode + '-läge.\
Sökningen genererade <b>' + format(len(results)) + '</b> träffar av\
 <b>' + str(result_limit) + '</b> möjliga. Gör en \
<a href="http://offentligautredningar.se/index.html">ny sökning</a>.</p>')
print("<br>")


def printhits():
    '''This only prints the metadata from the database. Fast.'''
    for result in results:
        fulltexturl = '<a href="http://offentligautredningar.se/source/' + result['filename'] + '"\
                        >' + result['filename'][:-4] + '</a>'
        year = str(result['year'])
        number = str(result['number'])

        print('<p>År: ' + year + ' Nummer: ' + number + ' Länk: \
                ' + fulltexturl + '</p>' )

def printcontext():
    '''This is a terribly slow proof-of-concept for printing context for
    each search result. The look-ahead/behind regex is terribly costly.'''
    regexpresult = 0
    for result in results:
        regexpresult += 1
        contextstring = "(.*)(" + search_string + ")(.*\n.*)"
        resultstring = re.findall(contextstring + '.*', result['fulltext'], re.IGNORECASE)
        fulltexturl = '<a href="http://offentligautredningar.se/source/' + result['filename'] + '"\
        >' + result['filename'][:-4] + '</a>'
        year = str(result['year'])
        number = str(result['number'])
        def iterateoverSOU():
            inSOUresults = 0
            outlist = []
            for r in resultstring:
                inSOUresults += 1
                outputprint = (str(inSOUresults) + ". " + r[0] + r[1] + r[2])
                outlist.append(outputprint)
            return(inSOUresults, outlist)
        print('<p>' + str(regexpresult) + '. <b>År:</b> ' + year + ', <b>Nummer\
                : </b>' + number +' ,<b>Fulltext:</b> ' + fulltexturl + '. <b>\
                ' + str(iterateoverSOU()[0]) + '</b> träffar.<br></p>')
        print('<textarea rows="10" cols="100">')
        for iteration in (iterateoverSOU()[1]):
            print(iteration)
        print('</textarea>')

# Just launching the two search modes depending on input from html form.
if metod == "simple":
    printhits()
elif metod == "advanced":
    printcontext()


#print(graphcontrol())
print('<br>Gör en <a href="http://offentligautredningar.se/index.html">ny sökning</a>.')

print('''
    <br>
    </body>
    </html>
    ''')
