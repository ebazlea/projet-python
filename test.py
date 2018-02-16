import sys
from PIL import Image

def pixelisation(im, radius):
 
    pixim = im.load()


    largeur = im.size[0]
    hauteur = im.size[1]
    cop = im.convert("L").copy()
    pixcop = cop.load()
    copyfinale = cop.copy()
    pixcopyfinale = copyfinale.load()
    
    for x in range(radius,largeur, radius*2+1):
        for y in range(radius,hauteur,radius*2+1):
            somme = 0 
            i = 0
          
            for X in range (x-radius, x+radius+1):
                if (0 <= X< largeur):
                   for Y in range(y-radius, y+radius+1):
                       if (0 <= Y < hauteur):
                           i += 1
                           somme += pixcop[X,Y]
        
            somme = somme//i
          

            for X in range (x-radius, x+radius+1):
                if (0 <= X< largeur):
                   for Y in range(y-radius, y+radius+1):
                       if (0 <= Y < hauteur):
                         pixcopyfinale[X,Y]= somme
            

        
            
    return copyfinale

im = Image.open(sys.argv[1])

num = int(sys.argv[2])
print("le nombre passé est ",num)
cop = pixelisation(im,num)
cop.show()


