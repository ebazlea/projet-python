from PIL import Image
import sys
import os
from os import listdir
from os.path import isfile, join

def decoupage(im, t):
    h = im.size[1]          #récupère la taille de l'image à decouper
    l = im.size[0]
    cop =im.copy()          #copy l'image
    largeur = l//t          #récupère la taille des images à découper
    hauteur = h//t
    for i in range (t):
        for j in range (t):
            left = i*largeur
            top = j*hauteur

            right = (i+1)*largeur
            bottom = (j+1)*hauteur

            petite = cop.crop((left, top, right, bottom))       #découpe la copie
            petite.save("decoupe/im_%d_%d.jpeg"%(i,j),"JPEG")   #enregistre la petites image( im_i_j.jpeg )dans le dossier "decoupe"

""" 
normalise les 3 histogrammes pour avoir des comparaisons cohérentes
"""

def normalize(h):
    s = sum(h)
    return [x*1000.0/s for x in h] #normalise 1 histo

def normalize3(H):
    return [normalize(h) for h in H] #normalise 3 histos


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
compare la distance entre 2 histogrammes
"""
def compare_histo(histo1, histo2):
    s = 0    
    for x,y in zip(histo1,histo2): 
        s+=abs(x-y) 
    return s

""" 
fait la comparaison entre les histogrammes de notre petite image et de toutes les images de la basse de donnée (et leurs histogrames)
remplace a par la plus petite distance que l'on trouve entre 2 histogrammes 
renvoi l'image dont les histogrames sont le plus proche ( la plus resemblante)


"""

def compare(petite, imgs, histos):
    a = 999999999999999999999999999 #initialisation au max
    j=None #initialisation image 
    hpetite = histo_hsv(petite) #creer les histogrammes de une des images découpée
    for im, him  in zip(imgs, histos): 
        s = compare_histo(hpetite[0], him[0])*6 #porte plus d'importance sur la couleur
        s += compare_histo(hpetite[1], him[1])
        s += compare_histo(hpetite[2], him[2])
        if (s<a):
            a=s
            j=im
    return j #renvoie l'image qui ressemble le plus


"""
remplace la petite image par l'image de la base de donnée correspondante
"""

def remplace(imgs, histos, t):  
    for X in range (t):
        for Y in range (t):
            name = "decoupe/im_%d_%d.jpeg"%(X,Y)    
            petite = Image.open(name)               
            Iname=compare(petite,imgs, histos)      
            if Iname:
                I = Image.open(Iname)
                oname = "replace/im_%d_%d.jpeg"%(X,Y)
                I.save(oname,"JPEG")                
            else:
                print("pas trouve d'images")


""" 
recolle les images decouper
"""
def recollage(im, t):
    h = im.size[1]      
    l = im.size[0]
    pix = Image.new('RGB',(l,h))    
    pixels = pix.load()
    largeur = l//t                 
    hauteur = h//t

    for X in range (t):                             
        for Y in range (t):

            name = "replace/im_%d_%d.jpeg"%(X,Y)    
            
            I = Image.open(name)
            Ir= I.resize((largeur,hauteur),Image.ANTIALIAS)   
            petite =Ir.load()
            

            for x in range(largeur): 
                for y in range(hauteur):

                    pixels[(X*largeur)+x,(Y*hauteur)+y]=petite[x,y]  

    return pix 


""" 
charge les histograme present dansle dossier histos
"""
def loadhistos(filename):
	histos=[]
	filename = 'histos/'+filename.replace(".jpeg", ".histo") 
	with open(filename) as f:
		for line in f:
			histos.append(list(map(float,line.split())))
	return histos


mypath = 'jpg'              
if len(sys.argv) > 3:
    mypath = sys.argv[3]

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith("jpeg")] 

histos = []    
for filename in onlyfiles:
	histos.append(loadhistos(filename)) 
print("histos done")


myim = Image.open(sys.argv[1]) 
myt = int(sys.argv[2])
decoupage(myim, myt) 
print("decoupe done")

remplace(onlyfiles,histos, myt) 
print("remplace done")

final = recollage(myim, myt) 
final.show()
print("recollage done")

