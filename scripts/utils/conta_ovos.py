import xml.etree.ElementTree as ET

folderes = os.listdir("noronha")

for folder in folderes:
cont_ovos = 0
for xml in xmls:
    if xml[-3:] == "xml":
       root = ET.parse(xml).getroot()
       try:
           cont = root.findall("object")
           cont_ovos +=len(cont) 
           if len(count) == 0:
              print("Encontrado", len(count))
       except:
             os.remove()
             print("Não encontrado")


