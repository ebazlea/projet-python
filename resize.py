import sys
from PIL import Image

def resize(im, radius):
    pixels=im.load()
    cop=Image.new("L",(radius,radius))
    pixelscop=cop.load()

    for y in range (radius) :
        for x in range (radius):
            pixelscop[x,y]=pixels[(x*im.size[0])//radius,(y*im.size[1])//radius]



    return cop
    pass#pass sert juste a ce que ca compile

im = Image.open(sys.argv[1])

num = int(sys.argv[2])
print("le nombre passé est ",num)
cop = resize(im,num)
cop.show()
