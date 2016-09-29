from os import listdir

counter = 0

for filename in listdir(u"//home/chrisk/www/offentligautredningar.se/source/"):
    with open("//home/chrisk/www/offentligautredningar.se/source/" + filename, encoding='utf-8') as currentfile:
        print(filename[:-3])
        text = currentfile.readlines()
        htmlfile = open('//home/chrisk/www/offentligautredningar.se/sourcehtml/' + filename[:-3] + 'html', 'w', encoding='utf-8')
        htmlfile.write('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
        for t in text:
            if t == "\n":
                #print(t + "<br>")
                htmlfile.write(t + "<br>")
            else:
                htmlfile.write(t)
                #print(t)
        htmlfile.close()
        counter += 1
        print("Done file " + str(counter)) 
        #print(text)
