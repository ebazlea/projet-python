import os
import sys
from PIL import Image

from os import listdir
from os.path import isfile, join


""" 
normalise les histogrammes pour avoir des comparaisons cohérentes
"""
def normalize(h): 
    s = sum(h)
    return [x*1000.0/s for x in h]

def normalize3(H): 
    return [normalize(h) for h in H]


""" 
cree les 3 histogrammes HSV
"""

def histo_hsv(im):
    imhsv = im.convert("RGB").convert("HSV")
    pixels = imhsv.load()                   
    tab = [[0] * 256 for x in range (3)]   
    for x in range (im.size[0]):
        for y in range (im.size[1]):        
            H,S,V=pixels[x,y]               
            tab[0][H]+=1                    
            tab[1][S]+=1
            tab[2][V]+=1
    return normalize3(tab)                  

    
""" 
enregistre les histogrames "hisos " dans le dossier "filename"
"""

def savehistos(histos,filename):
    with open(filename,'w')as f:
        for h in histos:
            print(*h,file=f)
            
         
         
mypath = 'imgs'                
if len(sys.argv) > 2:
    mypath = sys.argv[1]

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith("jpeg")]                     
print(*onlyfiles, sep="\n")
for filename in onlyfiles:              
    im = Image.open(filename)          
    h = histo_hsv(im)                   
    savehistos(h, 'histos/'+filename.replace(".jpeg", ".histo")) 
    print("save",'histos/'+filename)
print("histos done")
