import xml.etree.ElementTree as ET
import os
import argparse
import xml.etree


parser = argparse.ArgumentParser(description="Remove xmls without eggs", add_help=True)
parser.add_argument("--path", type=str, required=True, help="path to folders")
args = parser.parse_args()

print("Path: ", args.path)

folderes = os.listdir(args.path)

for folder in folderes:
    for xml in os.listdir(args.path+"/"+folder):
        if xml[-3:] == "xml":
            print("AQUI: ",args.path+"/"+folder+"/"+xml)

            root = ET.parse(args.path+"/"+folder+"/"+xml,  ET.XMLParser(encoding='utf-8')).getroot()

            count = root.findall("object")
            if len(count) > 0:
               print("Encontrado", len(count), " ovos em ", xml)
            
            else: 
                 try:
                    print("Removendo "+ args.path+"/"+folder+"/"+xml)
                    png = xml.replace("xml", "png")
                    os.remove(args.path+"/"+folder+"/"+xml)
                    os.remove(args.path+"/"+folder+"/"+png)
                
                 except:
                       print("Erro ao remover: ",  args.path+"/"+folder+"/"+xml)
                          
