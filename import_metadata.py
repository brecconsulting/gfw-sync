import csv


meta_lines = []
with open(r'C:\users\thomas.maschler\Desktop\WRI_metadata_gnq2.txt', 'r') as csvfile:
    meta = csv.reader(csvfile, delimiter='\t', quotechar='"')
    for row in meta:
        meta_lines.append(row)

meta_attribut = meta_lines[1:len(meta_lines)-1]

layers = meta_lines[0][1:len(meta_lines[0])-1]

meta = {}
i = 0

for layer in layers:
    meta[layer] = {}
    for att in meta_attribut:
        meta[layer][att[0]] = att[i+1]
    i +=1

print meta['concessions']