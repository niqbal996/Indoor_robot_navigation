from PIL import Image


size = 640,480

i= 1 

for i in range(1,79):
        im = Image.open("notdoor (" +str(i) +").jpg")
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save("notdoor_resized (" + str(i)+ ").jpg","JPEG")



