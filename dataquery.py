import pysolr


solr = pysolr.Solr('http://localhost:8983/solr/sou/', timeout=1000)

search_string = "1922"
result_limit = 10
order = "year asc"
depth = 10000000

results = solr.search(search_string, rows = result_limit, sort = order,
            **{
                'hl':'true',
                'hl.fragsize': 100,
                'hl.fl': 'year',
                'hl.maxAnalyzedChars': depth,
                'hl.snippets': 1000,
                })

for r in results:
    print(r['id'])
    print(r['year'])
    print(r['number'])
    print(r['filename'])
    print(r['pdfurl'])
    print("---") 
