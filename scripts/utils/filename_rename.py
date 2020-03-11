import xml.etree.ElementTree as ET
import os
import xml.etree as e 


folders = os.listdir("nova")
print(len(folders))
for folder in folders:
    for arq in os.listdir("nova/"+folder):
        if arq[-3:] == "xml":
           print(arq)
           et = ET.parse("nova/"+folder+"/"+arq)
           et.find('.//filename').text = arq.replace("xml", "png")
           et.write("nova/"+folder+"/"+arq)







