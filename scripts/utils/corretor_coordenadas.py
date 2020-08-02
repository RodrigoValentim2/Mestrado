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
                print("_______________________________________________________")
                print("XMIN: ", member.find('.//xmin').text)
                print("YMIN: ", member.find('.//ymin').text)
                print("XMAX: ", member.find('.//xmax').text)
                print("YMAX: ", member.find('.//ymax').text)
                member.find('.//xmin').text = member.find('.//xmin').text.split(".")[0]
                member.find('.//ymin').text = member.find('.//ymin').text.split(".")[0]
                member.find('.//xmax').text = member.find('.//xmax').text.split(".")[0]
                member.find('.//ymax').text = member.find('.//ymax').text.split(".")[0]
            print("Salavando: ", args.path+"/"+folder+"/"+xml)
            root.write(args.path+"/"+folder+"/"+xml)
        
