import xml.etree.ElementTree as ET
mytree = ET.parse('price.xml')
root = mytree.getroot()[0][0]
i = 0
items = []
for offer in root:
    item = {}
    for attr in offer:
        item[attr.tag] = attr.text
    items.append(item)
    i += 1
    if i == 500:
        break

print(items)