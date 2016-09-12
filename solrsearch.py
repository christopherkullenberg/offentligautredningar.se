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
from urllib.parse import urlencode
from urllib.request import urlopen
import simplejson
from collections import OrderedDict


# Fix IO and utf8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

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
    result_limit = 50

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
print('''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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

<a href="/"><div id="top">
	
	<div class="toppadding">
	<span class="icon">&#9737;</span> <h1>Offentliga utredningar</h1>
	</div>
	
</div> <!-- / top --></a>


<div class="sidebarinside">


<div id="searchbar">	
	
<div id="searchfield">
<form action="search" method="post">	
	<input type="text" name="search_word" value="''' + search_string + '''">

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

<!--
	<h5>Antal träffar</h5>

    Min. <input type="range" name="depth" min="100000" max="1000000" /> Max.

    <h5>Antal resultat</h5>
    <input type="number" name="result_limit" value=100 />
-->
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





<div id="topmaindiv">
<div class="topmaindivpadding">Ett gratis verktyg för att söka i statens offentliga utredningar. <a href="./om.html">Läs mer.</a></div>
</div>


	
<div id="maindiv">
		
	
<div id="maindivcontent">
''')

	
header = '''<div id="resulttable"><div class="resultinfo">
                <div class="result1">
                        <h3>Namn</h3>
                </div> <!-- / result1 -->

                <div class="result3">
                        <h3>PDF</h3>
                </div> <!-- / result3 -->

                <div class="result2">
                        <h3>Publicerad</h3>
                </div> <!-- / result2 -->
        </div> <!-- / result -->'''

def enkelsearch(searchword, start, rows):
    qstr = urlencode(OrderedDict([('q', searchword), 
                                ('wt', 'json'), 
                                #('sort', 'year asc'),
                                ('start', start),
                                ('rows', rows)]))
    return(qstr)

def printhits():
    #results = solr.search(search_string, rows = "30") #add sort=order to sort by order varialb3e
    connection = urlopen(u'http://localhost:8983/solr/sou/select?' + enkelsearch(search_string, 0, 24))
    results = simplejson.load(connection)
    print('''
    <div class="resulttitle"> <span class="resulttitletext">Hittade ''' + str(results['response']['numFound']) + ''' resultat.</span> </div> <!-- / resulttitle -->
    ''')
    print(header)
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

def avanceradsearch(searchword, start, rows):
    qstr = urlencode(OrderedDict([('q', searchword), 
                                ('wt', 'json'), 
                                ('sort', 'year asc'),
                                ('start', start),
                                ('rows', rows),
                                ('hl', 'true'),
                                ('hl.q', searchword),
                                ('hl.fl', 'fulltext'),
                                ('hl.fragsize', 100),
                                ('hl.snippets', 1000),
                                ('hl.maxAnalyzedChars', 1000000),
                                ('hl.simple.pre', '<mark>'),
                                ('hl.simple.post', '</mark>')
                                ]))
    return(qstr)



def printcontext():
    connection = urlopen(u'http://localhost:8983/solr/sou/select?' + avanceradsearch(search_string, 0, 9))
    results = simplejson.load(connection)
    resultcounter = 0
    yearlist = []
    print('''
    <div class="resulttitle"> <span class="resulttitletext">Hittade ''' + str(results['response']['numFound']) + ''' resultat.</span> </div> <!-- / resulttitle -->
    ''')
    print(header)
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

    #printgraph(yearlist)

'''
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
'''

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


print('''

</div> <!-- / resulttable -->	
</div> <!-- / maindivcontent -->
</div> <!-- / maindiv -->

</body>

</html>
    ''')
