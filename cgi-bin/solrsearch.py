#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgi, cgitb
import sys
import re
import os
from urllib.parse import urlencode
from urllib.request import urlopen
import urllib.parse
import simplejson
from collections import OrderedDict
from printhtml import header, header2, insearchheader, footer

# Fix IO and utf8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# get data from URL
formapi = cgi.FieldStorage()
query = formapi.getvalue('q')
if formapi.getvalue('start'):
    start = formapi.getvalue('start')
else:
    start = 0 
if formapi.getvalue('method'):
    method = formapi.getvalue('method')

if formapi.getvalue('order'):
    order = formapi.getvalue('order')

if formapi.getvalue('rows'):
    rows = formapi.getvalue('rows')
    if int(rows) > 100:
        rows = 100
else:
    rows = 24

# Get data from fields
form = cgi.FieldStorage()
if form.getvalue('q'):
    form_string = form.getvalue('q')
    search_string = form_string


#if form.getvalue('result_limit'):
#    result_limit = form.getvalue('result_limit')
#else:
#    result_limit = 50

if form.getvalue('method'):
    themethod = form.getvalue('method')
    if themethod == "simple":
        method = "simple"
    elif themethod == "advanced":
        method = "advanced"

if form.getvalue('order'):
    theorder = form.getvalue('order')
    if theorder == "year asc":
        order = "year asc"
    elif theorder == "year desc":
        order = "year desc"

if form.getvalue('depth'):
    depth = form.getvalue('depth')
else:
    depth = 100000



# This breaks the script to continue with a json print
if method == 'json':
    # Printjson needs search_string, order, start, rows
    from printjson import printjson
    print('Content-type:text/html; charset=utf-8\r\n\r\n')
    print(printjson(search_string, order, start, rows))
    sys.exit()


print(header())
#print(order)
print(search_string)
print(header2())


def enkelsearch(searchword, start, rows):
    qstr = urlencode(OrderedDict([('q', searchword), 
                                ('wt', 'json'), 
                                #('sort', 'year asc'),
                                ('start', start),
                                ('rows', rows)]))
    return(qstr)

def printhits():
    #results = solr.search(search_string, rows = "30") #add sort=order to sort by order varialb3e
    connection = urlopen(u'http://localhost:8983/solr/sou/select?' + enkelsearch(search_string, start, rows))
    results = simplejson.load(connection)
    numberofresults = results['response']['numFound']
    numres = numberofresults
    print('''
    <div class="resulttitle"> <span class="resulttitletext">Hittade ''' + str(numberofresults) + ''' resultat.</span> </div> <!-- / resulttitle -->
    ''')
    print(insearchheader())
    #<div class="resulttitle"> <span class="resulttitletext">Vi hittade 553 resultat:</span> </div> <!-- / resulttitle -->

    '''This only prints the metadata from the database. Fast.'''
    for result in results['response']['docs']:
        #print(result)

        fulltexturl = '<a href="http://offentligautredningar.se/sourcehtml/' + result['filename'][:-3] + 'html"\
                        ><h3>' + result['filename'][:-4] + '</h3></a>'
        year = str(result['year'])
        number = str(result['number'])
        print('''
        	<div class="result">
		<div class="result1">
			''' + fulltexturl + '''
		</div> <!-- / result1 -->
		
            ''')
        print('''
            <div class="result3">
	    <a href="''' + result['pdfurl'] + '''"><h5>Ladda ner</h5></a>
	    </div> <!-- / result1 -->
            ''')
        print('''
		<div class="result2">
			<h4>År: '''+ year + '''  Nummer: ''' + number + '''</h4>
		</div> <!-- / result1 -->
	</div> <!-- / result -->
            ''')
    starturl = -25
    pages = 0
    nextpage = starturl + 50
    for iteration in range(round(numberofresults / 25)):
        pages += 1
        starturl += 25
        print('<a href="http://offentligautredningar.se/search?q=' + urllib.parse.quote(search_string) + '&start=''' + str(starturl) + '&method=simple">' + str(pages) + '</a>')
    print('<a href="http://offentligautredningar.se/search?q=' + urllib.parse.quote(search_string) + '&start=' + str(nextpage) + '&method=simple">' + "Nästa" + '</a>')

def avanceradsearch(searchword, order,  start, rows):
    qstr = urlencode(OrderedDict([('q', searchword), 
                                ('wt', 'json'), 
                                ('sort', order),
                                ('start', start),
                                ('rows', rows),
                                ('hl', 'true'),
                                ('hl.q', searchword),
                                ('hl.fl', 'fulltext'),
                                ('hl.fragsize', 200),
                                ('hl.snippets', 10),
                                ('hl.maxAnalyzedChars', 1000000),
                                ('hl.simple.pre', '<mark>'),
                                ('hl.simple.post', '</mark>')
                                ]))
    return(qstr)



def printcontext():
    connection = urlopen(u'http://localhost:8983/solr/sou/select?' + avanceradsearch(search_string, order, start, rows))
    results = simplejson.load(connection)
    resultcounter = 0
    yearlist = []
    numberofresults = results['response']['numFound']
    print('''
    <div class="resulttitle"> <span class="resulttitletext">Hittade ''' + str(numberofresults) + ''' resultat.</span> </div> <!-- / resulttitle -->
    ''')
    print(insearchheader())
    #print(results['response']['start'], "start")
    for result in results['response']['docs']:
        resultcounter += 1
        fulltexturl = '<a href="http://offentligautredningar.se/sourcehtml/' + result['filename'][:-3] + 'html"\
        >' + result['filename'][:-4] + '</a>'
        databaseid = str(result['id']) #for debugging
        year = str(result['year'])
        yearlist.append(year)
        number = str(result['number'])
        print('''
                <div class="result">
                <div class="result1">
                        ''' + fulltexturl + '''

            ''')
          
        for f, v in results['highlighting'][result['id']].items():
            print("<p>" +  v[0] + "</p>")

        print('</div>')
        print('''
            <div class="result3">
            <a href="''' + result['pdfurl'] + '''"><h5>Ladda ner</h5></a>
            </div> <!-- / result1 -->
            ''')
        print('''
                <div class="result2">
                        <h4>År: '''+ year + '''  Nummer: ''' + number + '''</h4>
        
            ''')
        print('</div></div>')
    starturl = -int(rows) 
    pages = 0
    nextpage = int(starturl) + int(rows)
    for iteration in range(round(numberofresults / int(rows))):
        pages += 1
        starturl += int(rows)
        print('<a href="http://offentligautredningar.se/search?q=' + urllib.parse.quote(search_string) + '&start=' + str(starturl) + '&method=advanced&order=' + order + '">' + str(pages) + '</a>')
    print('<a href="http://offentligautredningar.se/search?q=' + urllib.parse.quote(search_string) + '&start=' + str(nextpage) + '&method=advanced&order=' + order + '">' + "Nästa" + '</a>')


# Just launching the two search modes depending on input from html form.
#method = "simple"
if method == "simple":
    printhits()
elif method == "advanced":
    printcontext()

print(footer())
