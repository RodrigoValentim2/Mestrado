import xml.etree.ElementTree as ET
import os
import argparse
import xml.etree
import pandas as pd

parser = argparse.ArgumentParser(description="Cria um csv com (nome da image, quantidade de ovos)", add_help=True)
parser.add_argument("--path", type=str, required=True, help="path to folders")
args = parser.parse_args()

print("Path: ", args.path)

folderes = os.listdir(args.path)
names = []
qtds = []
for folder in folderes:
    for xml in os.listdir(args.path+"/"+folder):
        if xml[-3:] == "xml":
     
            root = ET.parse(args.path+"/"+folder+"/"+xml,  ET.XMLParser(encoding='utf-8')).getroot()

            count = root.findall("object")
            xmin = root.findall("xmin")
            print(xml, " ", count[0][4][0].text)
            if len(count) > 0:
               names.append(xml)
               qtds.append(len(count))

result = {"imagem": names, "quantidade_ovos":qtds}

df = pd.DataFrame(result)

df.to_csv("data.csv", index=None)



                          
