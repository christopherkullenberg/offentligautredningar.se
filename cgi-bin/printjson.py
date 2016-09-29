from urllib.parse import urlencode
from urllib.request import urlopen
from collections import OrderedDict
import simplejson


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

def printjson(search_string, order, start, rows):
    import json
    connection = urlopen(u'http://localhost:8983/solr/sou/select?' + avanceradsearch(search_string, order, start, rows))
    results = simplejson.load(connection)
    resultcounter = 0
    yearlist = []
    numberofresults = results['response']['numFound']
    for result in results['response']['docs']:
        fulltexturl = '<a href="http://offentligautredningar.se/sourcehtml/' + result['filename'][:-3] + 'html"\
        >' + result['filename'][:-4] + '</a>'
        databaseid = str(result['id']) #for debugging
        year = str(result['year'])
        number = str(result['number'])
        pdfurl = result['pdfurl']
    starturl = 0
    pages = 1
    nextpage = int(starturl) + int(rows)
    starturl += int(rows)
    nextpage = 'http://offentligautredningar.se/search?q=' + search_string + '&start=' + str(nextpage) + '&method=json&order=' + order

    #printvariable = ['hej']
    data = {'databaseid': databaseid,
            'year': year,
            'number': number,
            'filename': result['filename'],
            'pdfurl': pdfurl,
            'nextpage': nextpage}
    printvariable = json.dumps(data, indent=4, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return(printvariable)
