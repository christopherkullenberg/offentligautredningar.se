from urllib import urlopen

f = urlopen("http://regina.kb.se/sou/")
lines = f.readlines()

for i in range(len(lines)-1):
  if not "urn:nbn:se:kb:sou" in lines[i]:
    continue
  parts = lines[i].split("\"")
  if "div" in parts[0]:
    url = parts[1]
  else:
    url = parts[2]
  data   = lines[i+1].split("\"")[1].replace("<",">").split(">")
  sou    = data[1]
  title  = data[3].strip()
  try:
    tf     = urlopen(url)
    temp   = tf.read()
  except:
    continue
  pdfurl = ""
  for t in temp.split("\""):
    if ".pdf" in t:
      pdfurl = t
      break
print("wget -O \"" + title + " - SOU "+ sou + ".pdf\" "+pdfurl)
