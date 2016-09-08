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


solr = pysolr.Solr('http://localhost:8983/solr/souprototype/', timeout=1000)

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
    if themetod == "red":
        metod = "simple"
    elif themetod == "green":
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

if form.getvalue('depth'):
    depth = form.getvalue('depth')
else:
    depth = 100000

if form.getvalue('output'):
    theoutput = form.getvalue('output')
    if theoutput == "show":
        output = "show"
    elif theoutput == "csv":
        output = "csv"
    elif theoutput == "tsv":
        output = "tsv"
    elif theoutput == "text":
        output = "text"
    elif theoutput == "json":
        output = "json"
else:
    output = "show"



# Change this when there are multiple modes
#mode = 'match'


# Print HTML
## Change directories for css and cgi-bin
print("Content-type:text/html; charset=utf-8\r\n\r\n")
print('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="sv-SE">

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width" />

<title>Sök i statens offentliga utredningar</title>

<link rel="stylesheet" href="./style.css" type="text/css" media="screen" />

<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico">

<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>



<!-- Radio buttons by: http://cssdeck.com/user/ftntravis -->

<script type="text/javascript">
$(document).ready(function(){
    $('input[type="radio"]').click(function(){
        if($(this).attr("value")=="red"){
            $(".box").not(".red").hide();
            $(".red").show();
        }
        if($(this).attr("value")=="green"){
            $(".box").not(".green").hide();
            $(".green").show();
        }
        if($(this).attr("value")=="blue"){
            $(".box").not(".blue").hide();
            $(".blue").show();
        }
    });
});
</script>


</head>

<body>




<div id="sidebar">

<div id="top">

	<div class="toppadding">
	<span class="icon">&#9737;</span> <h1>Offentliga utredningar</h1>
	</div>

</div> <!-- / top -->


<div class="sidebarinside">


<div id="searchbar">

<div id="searchfield">
<form action="search" method="post">
	<input type="text" name="search_word" placeholder="Vad söker du efter?">

</div> <!-- / searchfield -->


<div id="searchoptions">

<div class="searchtype">
<input type="radio" name="metod" id="radio1" class="radio" value="red" checked/>
<label for="radio1">Enkel</label>
</div>

<div class="searchtype">
<input type="radio" name="metod" id="radio2" class="radio" value="green" />
<label for="radio2">Avancerad</label>
</div>

</div> <!-- / searchoptions -->


<div id="utokadsokning">

    <div class="red box"><!--Placeholder for 'enkel'--></div>
    <div class="green box">

	<h5>Antal träffar</h5>

    Min. <input type="range" name="depth" min="100000" max="1000000" /> Max.

    <h5>Antal resultat</h5>
    <input type="number" name="result_limit" value=100 />

    <h5>Datumordning, årtal</h5>
    <p><input type="radio" name="order" value="Stigande" checked /> Stigande
    <input type="radio" name="order" value="Fallande" /> Fallande</p>

    </div> <!-- / green box -->

</div> <!-- / utokadsokning -->




<div id="searchbutton">
<input type="submit" value="Utför sökning" class="sun-flower-button">
</div> <!-- / searchbutton -->


</div> <!-- / searchbar -->


</div> <!-- / sidebarinside -->
</div> <!-- / sidebar -->

<div id="maindiv">


<div id="topmaindiv">
<div class="topmaindivpadding">Ett gratis verktyg för att söka i statens offentliga utredningar. <a href="#">Läs mer.</a></div>
</div>


<div id="maindivcontent">

<div id="resulttable">
    ''')


def printgraph(listofyears):
    import vincent
    from collections import Counter
    year_freq = Counter(listofyears).most_common(100)
    print(year_freq)
    labels, freq = zip(*year_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    #print(bar)
    #print(bar.to_json())
    bar.to_json('../results/bar.json')
  

'''
def printgraph(yearlist)
    tweet_freq = Counter(yearlist).most_common(10)
    #print(word_freq)
    labels, freq = zip(*tweet_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('tweet_freq.json')
'''




def printhits():
    results = solr.search(search_string, rows = result_limit, sort = order)
    '''This only prints the metadata from the database. Fast.'''
    for result in results:
        #print(result)

        fulltexturl = '<a href="http://offentligautredningar.se/source/' + result['filename'] + '"\
                        >' + result['filename'][:-4] + '</a>'
        year = str(result['year'])
        number = str(result['number'])

        print('<div class="resultinfo"><div class="result1"><h3>' + fulltexturl + '\
        </h3></div><div class="result2"><h4>År: ' + year + ' Nummer: ' + number + '\
        </h4></div></div>')


def printcontext():
    results = solr.search(search_string, rows = result_limit, sort = order,
                **{
                    'hl':'true',
                    'hl.fragsize': 100,
                    'hl.fl': 'fulltext',
                    'hl.maxAnalyzedChars': depth,
                    'hl.snippets': 1000,
                    })
    highlights = results.highlighting
    #print("test")
    resultcounter = 0
    print("Sökningen gav {0} träffar.".format(len(results)))
    print("Du sökte på <b>" + search_string + "</b> med djupet " + str(depth) + " tecken")
    yearlist = []
    for result in results:
        resultcounter += 1
        fulltexturl = '<a href="http://offentligautredningar.se/source/' + result['filename'] + '"\
        >' + result['filename'][:-4] + '</a>'
        databaseid = str(result['id']) #for debugging
        year = str(result['year'])
        yearlist.append(year)
        number = str(result['number'])
        print('<div class="resultinfo"><div class="result1"><h3>' + str(resultcounter) + '. ' + fulltexturl + '\
                </h3></div><div class="result2"><h4>År: ' + year + ' Nummer: ' + number + '\
                </h4></div></div>')

        ''' #Old print function
        print('<p>' + str(resultcounter) + '. <b>År:</b> ' + year + ', <b>Nummer\
                : </b>' + number +' ,<b>Fulltext:</b> ' + fulltexturl + '. <b>\
                </b>.<br></p>')
        '''
        print('<div class="resultinfo"><div class="result1">')
        #inSOUresults = 1 #for debugging
        for idnumber, h in highlights.items():
            if idnumber == databaseid:
                for key, value in h.items():
                    for v in value:
                        print("<p>" +  v + "</p>")
                        #inSOUresults += 1 #for debugging
        print('</div></div>')
    printgraph(yearlist)


def printcsv():
    import csv
    import time
    ts = int(time.time())
    print('Ladda ned filen <a href="http://offentligautredningar.se/results/' + str(ts) + '.csv">här</a>.')
    csvfile = open('../results/' + str(ts) + '.csv', 'w', encoding="utf-8")
    fieldnames = ['databaseid', 'year', 'number', 'result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"')
    writer.writeheader()
    results = solr.search(search_string, rows = result_limit, sort = order,
                **{
                    'hl':'true',
                    'hl.fragsize': 100,
                    'hl.fl': 'fulltext',
                    'hl.maxAnalyzedChars': depth,
                    'hl.snippets': 1000,
                    })
    highlights = results.highlighting
    for result in results:
            databaseid = str(result['id']) #for debugging
            year = str(result['year'])
            number = str(result['number'])
            for idnumber, h in highlights.items():
                if idnumber == databaseid:
                    for key, value in h.items():
                        for v in value:
                            writer.writerow({'databaseid': databaseid, 'year': year, 'number': number, 'result': v})
    csvfile.close()


def printtsv():
    import csv
    import time
    ts = int(time.time())
    print('Ladda ned filen <a href="http://offentligautredningar.se/results/' + str(ts) + '.tsv">här</a>.')
    csvfile = open('../results/' + str(ts) + '.tsv', 'w', encoding="utf-8")
    fieldnames = ['databaseid', 'year', 'number', 'result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    results = solr.search(search_string, rows = result_limit, sort = order,
                **{
                    'hl':'true',
                    'hl.fragsize': 100,
                    'hl.fl': 'fulltext',
                    'hl.maxAnalyzedChars': depth,
                    'hl.snippets': 1000,
                    })
    highlights = results.highlighting
    for result in results:
            databaseid = str(result['id']) #for debugging
            year = str(result['year'])
            number = str(result['number'])
            for idnumber, h in highlights.items():
                if idnumber == databaseid:
                    for key, value in h.items():
                        for v in value:
                            writer.writerow({'databaseid': databaseid, 'year': year, 'number': number, 'result': v})
    csvfile.close()


def printtext():
    import time
    ts = int(time.time())
    print('Ladda ned filen <a href="http://offentligautredningar.se/results/' + str(ts) + '.txt">här</a>.')
    txtfile = open('../results/' + str(ts) + '.txt', 'w', encoding="utf-8")
    results = solr.search(search_string, rows = result_limit, sort = order,
                **{
                    'hl':'true',
                    'hl.fragsize': 100,
                    'hl.fl': 'fulltext',
                    'hl.maxAnalyzedChars': depth,
                    'hl.snippets': 1000,
                    })
    highlights = results.highlighting
    for result in results:
            databaseid = str(result['id']) #for debugging
            year = str(result['year'])
            number = str(result['number'])
            for idnumber, h in highlights.items():
                if idnumber == databaseid:
                    for key, value in h.items():
                        for v in value:
                            txtfile.write(databaseid + ", " + year + ", " +  number + ", " +  v + "\n")
    txtfile.close()


def printjson():
    import json
    import time
    ts = int(time.time())
    print('Ladda ned filen <a href="http://offentligautredningar.se/results/' + str(ts) + '.json">här</a>.')
    jsonfile = open('../results/' + str(ts) + '.json', 'w', encoding="utf-8")
    results = solr.search(search_string, rows = result_limit, sort = order,
                **{
                    'hl':'true',
                    'hl.fragsize': 100,
                    'hl.fl': 'fulltext',
                    'hl.maxAnalyzedChars': depth,
                    'hl.snippets': 1000,
                    })
    highlights = results.highlighting
    for result in results:
            databaseid = str(result['id']) #for debugging
            year = str(result['year'])
            number = str(result['number'])
            for idnumber, h in highlights.items():
                if idnumber == databaseid:
                    for key, value in h.items():
                        for v in value:
                            data = {
                            'databaseid': databaseid,
                            'year': year,
                            'number': number,
                            'result': v
                            }
                            json.dump(data, jsonfile, indent=4, sort_keys=True,
                            separators=(',', ':'), ensure_ascii=False)
    jsonfile.close()


# Just launching the two search modes depending on input from html form.
#metod = "simple"
if output == "show":
    if metod == "simple":
        printhits()
    elif metod == "advanced":
        printcontext()
elif output == "csv":
    printcsv()
elif output == "tsv":
    printtsv()
elif output == "text":
    printtext()
elif output == "json":
    printjson()

#print(graphcontrol())
print('<br>Gör en <a href="http://offentligautredningar.se/index.html">ny sökning</a>.')

print('''
</div> <!-- / maindivcontent -->
</div> <!-- / maindiv -->
</body>
</html>

    ''')
