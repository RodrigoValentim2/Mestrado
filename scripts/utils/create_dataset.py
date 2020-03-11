import os 

folders = os.listdir('nova')

try:
    # Create target Directory
    os.mkdir('dataset')
    if os.path.exists('dataset'):
        os.mkdir('dataset/images')
        os.mkdir('dataset/annotations')
        print("Directory Created ") 
except FileExistsError:
    print("Directories already exists")

for folder in folders:
    files = os.listdir('nova/'+folder)
    xml_files = []
    png_files = []
    for file in files:
        if file.endswith('.xml'):
            xml_files.append(file)
        else:
            png_files.append(file) 
    print(png_files)   
    print(xml_files)      
    for xml_file in xml_files:
        print(xml_file)
        name = xml_file.split('.')[0]
        if(name+'.png' in png_files):
            ind = png_files.index(name+'.png')
            os.popen(f'cp nova/{folder}/{png_files[ind]} dataset/images/{png_files[ind]} ') 
            os.popen(f'cp nova/{folder}/{xml_file} dataset/annotations/{xml_file} ')
