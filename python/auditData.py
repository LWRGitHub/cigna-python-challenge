import csv
import json
import xml.etree.ElementTree as ET
import yaml

with open('data.csv', 'r') as f:
    data = list(csv.reader(f))
    nodeAvgDividedByDict, allAvgDividedBy = {}, 0
    minMaxAvg = {
        'all': {
            'min': float(data[1][1]),
            'max': float(data[1][1]),
            'avg': 0
        }
    }

    for i in range(len(data[0])):
        if(i ==0): continue
        idx, nodeAvgDividedByDict[data[0][i]] = 1, 0
        if(data[1][i] == ''): 
            while(data[idx][i] == ''): idx += 1
        minMaxAvg[data[0][i]] = {
            'min': float(data[idx][i]),
            'max': float(data[idx][i]),
            'avg': 0
        }

    for i in range(len(data)-1):
        if(i == 0): continue
        for j in range(len(data[i])):
            if(j == 0 or data[i][j] == ''): continue
            if(float(data[i][j]) < minMaxAvg[data[0][j]]['min']):
                minMaxAvg[data[0][j]]['min'] = float(data[i][j])
                if(float(data[i][j]) < minMaxAvg['all']['min']): minMaxAvg['all']['min'] = float(data[i][j])
            if(float(data[i][j]) > minMaxAvg[data[0][j]]['max']):
                minMaxAvg[data[0][j]]['max'] = float(data[i][j])
                if(float(data[i][j]) > minMaxAvg['all']['max']): minMaxAvg['all']['max'] = float(data[i][j])

            minMaxAvg[data[0][j]]['avg'] += float(data[i][j])
            nodeAvgDividedByDict[data[0][j]] += 1
            minMaxAvg['all']['avg'] += float(data[i][j])
            allAvgDividedBy += 1
    
    # get average
    minMaxAvg['all']['avg'] = minMaxAvg['all']['avg'] / allAvgDividedBy
    for key in minMaxAvg:
        if(key == 'all'): continue
        minMaxAvg[key]['avg'] = minMaxAvg[key]['avg'] / nodeAvgDividedByDict[key]
    
    # write to file
    def writeToFile(path, data):
        with open(path, 'w') as file:
            json.dump(data, file)
            file.close()

    # .json file
    writeToFile('minMaxAvg.json', minMaxAvg)  

    # .xml file
    root = ET.Element('root')
    for key in minMaxAvg:
        node = ET.SubElement(root, 'node')
        node.set('name', key)
        node.set('min', str(minMaxAvg[key]['min']))
        node.set('max', str(minMaxAvg[key]['max']))
        node.set('avg', str(minMaxAvg[key]['avg']))
    tree = ET.ElementTree(root)
    tree.write('minMaxAvg.xml')

    # .yaml file
    with open('minMaxAvg.yaml', mode='w') as file:
        yaml.dump(minMaxAvg, file, indent=4)
        file.close()

    # .txt file
    writeToFile('minMaxAvg.txt', minMaxAvg)  

    f.close()

