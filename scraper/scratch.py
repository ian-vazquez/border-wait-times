import requests

url = "https://bwt.cbp.gov/api/bwtrss/rssbyportnum/HTML/ALL/240203"
response = requests.get(url)
print(response.text)

description = response.text.split("<description>")[2]
description = description.split("</description>")[0]

lines = description.split("<br/>")
for line in lines:
    print(repr(line.strip()))

currentCategory = None
currentLane = None
for line in lines:
    if ("<h4>") in line:
        temp = line.split("</b")[0].split("<b>")
        currentCategory = temp[1]
        
    elif ("Lanes:") in line:
        temp = line.split("Lanes:")
        currentLane = (temp[0] + temp[1])
        print(currentCategory + currentLane)

    

