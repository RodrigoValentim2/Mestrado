import xml.etree.ElementTree as ET
import os
import argparse
import xml.etree
import pandas as pd

parser = argparse.ArgumentParser(description="Corrige coordenadas com pontos flutuantes", add_help=True)
parser.add_argument("--path", type=str, required=True, help="path to folders")
args = parser.parse_args()

print("Path: ", args.path)

folderes = os.listdir(args.path)
names = []
qtds = []
for folder in folderes:
    for xml in os.listdir(args.path+"/"+folder):
        if xml[-3:] == "xml":
            root = ET.parse(args.path+"/"+folder+"/"+xml,  ET.XMLParser(encoding='utf-8'))
            et = ET.parse(args.path+"/"+folder+"/"+xml)
            
            for member in root.findall("object"):
                xmin = int(member.find('.//xmin').text)
                ymin = int(member.find('.//ymin').text)
                xmax = int(member.find('.//xmax').text)
                ymax = int(member.find('.//ymax').text)
                size = (xmax-xmin)*(ymax-ymin)
                print("Size: ",(xmax-xmin), " ",(ymax-ymin) )
        
